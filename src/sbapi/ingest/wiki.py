"""
Page sources. Both yield Page(title, wikitext, categories) so extraction
doesn't care where a page came from.

- WikiClient: the live MediaWiki API (api.php). Polite by construction:
  checks robots.txt for its own user agent, waits between requests, sends
  maxlag, and caches every response on disk so a re-run hits the network
  only for what it hasn't seen.
- read_dump: a MediaWiki XML dump (Special:Statistics on Fandom). No network.
"""

import bz2
import gzip
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_WIKI = "https://spaceballs.fandom.com"
USER_AGENT = "sbapi-ingest/0.1 (+https://github.com/thestackshepherd/sbapi)"

CATEGORY_LINK = re.compile(r"\[\[\s*Category\s*:\s*([^\]|]+)", re.IGNORECASE)


@dataclass
class Page:
    title: str
    wikitext: str
    categories: list[str] = field(default_factory=list)


class RobotsDisallowed(Exception):
    pass


class WikiClient:
    def __init__(self, base_url=DEFAULT_WIKI, cache_dir=".cache/wiki",
                 delay=1.0, user_agent=USER_AGENT):
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}/api.php"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.delay = delay
        self.user_agent = user_agent
        self._last_request = 0.0
        self._robots = None

    # -- plumbing --------------------------------------------------------

    def _check_robots(self, url):
        if self._robots is None:
            self._robots = urllib.robotparser.RobotFileParser()
            req = urllib.request.Request(f"{self.base_url}/robots.txt",
                                         headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=30) as resp:
                self._robots.parse(resp.read().decode("utf-8").splitlines())
            crawl_delay = self._robots.crawl_delay(self.user_agent)
            if crawl_delay:
                self.delay = max(self.delay, float(crawl_delay))
        if not self._robots.can_fetch(self.user_agent, url):
            raise RobotsDisallowed(f"robots.txt disallows {url} for {self.user_agent}")

    def _get(self, params):
        params = {**params, "format": "json", "formatversion": "2", "maxlag": "5"}
        query = urllib.parse.urlencode(sorted(params.items()))
        url = f"{self.api_url}?{query}"
        cached = self.cache_dir / (hashlib.sha256(query.encode()).hexdigest() + ".json")
        if cached.exists():
            return json.loads(cached.read_text())

        self._check_robots(url)
        for attempt in range(5):
            wait = self.delay - (time.monotonic() - self._last_request)
            if wait > 0:
                time.sleep(wait)
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=60) as resp:
                self._last_request = time.monotonic()
                data = json.loads(resp.read())
            if data.get("error", {}).get("code") == "maxlag":
                time.sleep(5 * (attempt + 1))
                continue
            if "error" in data:
                raise RuntimeError(f"API error for {url}: {data['error']}")
            cached.write_text(json.dumps(data))
            return data
        raise RuntimeError(f"Server stayed lagged for {url}")

    def _query_all(self, params):
        """Follow `continue` tokens until the list is exhausted."""
        cont = {}
        while True:
            data = self._get({**params, **cont})
            yield data
            if "continue" not in data:
                return
            cont = data["continue"]

    # -- what the pipeline uses -------------------------------------------

    def license(self):
        """The wiki's declared content license (siteinfo rightsinfo)."""
        data = self._get({"action": "query", "meta": "siteinfo", "siprop": "rightsinfo|general"})
        return {"license": data["query"]["rightsinfo"],
                "sitename": data["query"]["general"].get("sitename")}

    def category_members(self, category):
        titles = []
        for data in self._query_all({"action": "query", "list": "categorymembers",
                                     "cmtitle": f"Category:{category}",
                                     "cmnamespace": "0", "cmlimit": "500"}):
            titles += [m["title"] for m in data["query"]["categorymembers"]]
        return titles

    def pages(self, titles):
        """Fetch wikitext + categories, 50 titles per request (the API's limit)."""
        titles = list(dict.fromkeys(titles))
        for i in range(0, len(titles), 50):
            batch = titles[i:i + 50]
            data = self._get({"action": "query", "prop": "revisions|categories",
                              "rvprop": "content", "rvslots": "main",
                              "cllimit": "max", "redirects": "1",
                              "titles": "|".join(batch)})
            for p in data["query"].get("pages", []):
                if p.get("missing") or not p.get("revisions"):
                    continue
                text = p["revisions"][0]["slots"]["main"]["content"]
                cats = [c["title"].split(":", 1)[1] for c in p.get("categories", [])]
                yield Page(p["title"], text, cats)


def read_dump(path):
    """Yield main-namespace pages from a MediaWiki XML dump (.xml, .gz or .bz2)."""
    path = str(path)
    opener = gzip.open if path.endswith(".gz") else bz2.open if path.endswith(".bz2") else open
    with opener(path, "rb") as fh:
        title = ns = text = None
        for _, el in ET.iterparse(fh, events=("end",)):
            tag = el.tag.rsplit("}", 1)[-1]
            if tag == "title":
                title = el.text
            elif tag == "ns":
                ns = el.text
            elif tag == "text":
                text = el.text or ""
            elif tag == "page":
                if ns == "0" and text and not text.lstrip().upper().startswith("#REDIRECT"):
                    cats = [c.strip() for c in CATEGORY_LINK.findall(text)]
                    yield Page(title, text, cats)
                title = ns = text = None
                el.clear()


def page_url(base_url, title):
    return f"{base_url.rstrip('/')}/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
