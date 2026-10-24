"""
Tests for the ingest pipeline. The load test needs Postgres: set SBAPI_TEST_DSN,
e.g. postgresql://postgres:postgres@localhost/sbapi_dev_db. It works in a
throwaway schema and drops it afterwards.
"""

import json
import os
from pathlib import Path

import pytest

from sbapi.ingest import extract, validate, wiki
from sbapi.ingest.__main__ import read_records

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample"
BASE = "https://spaceballs.fandom.com"

# Shaped like a Fandom portable infobox page. Values are from the wiki's Barf page.
BARF_WIKITEXT = """{{Quote|Oh! That's gonna leave a mark.|[[Barf]]}}
{{Infobox character
|image = Barf.jpg
|real name = Barfolomew
|species = Mawg
|occupation = Co-pilot
|actor = [[John Candy]]
|appearances = [[Spaceballs]]
|favourite food = unmapped on purpose
}}
'''Barfolomew''', nicknamed '''Barf''', was [[Lone Starr]]'s best friend and co-pilot.<ref>[https://example.org/script Spaceballs script]</ref>

== Behind the scenes ==
* Rick Moranis suggested [[John Candy]] for the role of Barf.<ref name="a">Commentary</ref>
* His ears were controlled by Creature FX Puppeteer Rick Lazzarini.<ref name="a"/>

== Trivia ==
* Barf's rank on the 5-Man Band would be the Big Guy.

[[Category:Characters]]
"""


def test_extract_character():
    page = wiki.Page("Barf", BARF_WIKITEXT, ["Characters"])
    record, etype, quotes, unmapped = extract.extract(page, BASE)
    assert etype == "character"
    assert validate.errors("character", record) == []
    assert record["full_name"] == "Barfolomew"
    assert record["species"] == "Mawg"
    assert record["character_role"] == "Co-pilot"
    assert record["homeworld"] is None and record["gender"] is None  # not stated, so not guessed
    assert record["appears_in"] == ["Spaceballs"]
    assert record["portrayed_by"] == [{"actor_name": "John Candy", "media_title": None,
                                       "credit_type": None, "notes": None}]
    assert record["image_url"] == f"{BASE}/wiki/Special:FilePath/Barf.jpg"
    assert [t["kind"] for t in record["trivia"]] == ["behind_the_scenes", "behind_the_scenes", "trivia"]
    assert record["trivia"][0]["text"] == "Rick Moranis suggested John Candy for the role of Barf."
    assert [(c["number"], c["text"], c["url"]) for c in record["citations"]] == [
        (1, "Spaceballs script", "https://example.org/script"), (2, "Commentary", None)]
    assert unmapped == ["favouritefood"]
    assert quotes == [{"quote_text": "Oh! That's gonna leave a mark.", "character_name": "Barf",
                       "media_title": None, "episode_title": None, "citations": [],
                       "source_url": f"{BASE}/wiki/Barf"}]


def test_uncategorised_page_is_skipped():
    record, etype, _, _ = extract.extract(wiki.Page("Some page", "Text.", ["Images"]), BASE)
    assert record is None and etype is None


def test_read_dump(tmp_path):
    dump = tmp_path / "dump.xml"
    dump.write_text(f"""<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.11/">
  <page><title>Barf</title><ns>0</ns><revision><text>{BARF_WIKITEXT.replace('&', '&amp;').replace('<', '&lt;')}</text></revision></page>
  <page><title>Template:Quote</title><ns>10</ns><revision><text>x</text></revision></page>
  <page><title>Barfolomew</title><ns>0</ns><revision><text>#REDIRECT [[Barf]]</text></revision></page>
</mediawiki>""")
    pages = list(wiki.read_dump(dump))
    assert [p.title for p in pages] == ["Barf"]
    assert pages[0].categories == ["Characters"]


def test_sample_records_are_valid():
    records = read_records(SAMPLE)
    assert records
    for etype, recs in records.items():
        for rec in recs:
            assert validate.errors(etype, rec) == [], rec["source_url"]


@pytest.mark.skipif(not os.getenv("SBAPI_TEST_DSN"), reason="needs SBAPI_TEST_DSN")
def test_load_is_idempotent():
    import psycopg

    from sbapi.ingest.load import Loader

    schema_sql = (ROOT / "src/sbapi/app/database/sbapidatabase_schema.sql").read_text()
    tables = ["media", "actors", "characters", "vehicles", "quotes", "trivia",
              "character_actors", "media_characters", "media_vehicles", "vehicle_crew"]

    with psycopg.connect(os.environ["SBAPI_TEST_DSN"], autocommit=True) as conn:
        cur = conn.cursor()
        cur.execute("DROP SCHEMA IF EXISTS ingest_test CASCADE; CREATE SCHEMA ingest_test")
        cur.execute("SET search_path TO ingest_test")
        try:
            cur.execute(schema_sql)
            records = read_records(SAMPLE)
            Loader(conn).load(records)
            first = _snapshot(cur, tables)
            Loader(conn).load(records)
            assert _snapshot(cur, tables) == first

            cur.execute("SELECT count(*) FROM vehicle_crew")
            assert cur.fetchone()[0] == 2
            cur.execute("SELECT a.actor_name FROM character_actors ca JOIN actors a ON a.id = ca.actor_id "
                        "JOIN characters c ON c.id = ca.character_id WHERE c.character_name = 'Barf'")
            assert cur.fetchall() == [("John Candy",)]
        finally:
            cur.execute("DROP SCHEMA ingest_test CASCADE")


def _snapshot(cur, tables):
    """Every row of every table, minus last_updated (which a re-run refreshes)."""
    out = {}
    for t in tables:
        cur.execute(f"SELECT * FROM {t}")
        names = [d.name for d in cur.description]
        out[t] = sorted(json.dumps({k: v for k, v in zip(names, row) if k != "last_updated"},
                                   default=str, sort_keys=True) for row in cur.fetchall())
    return out


def test_wiki_client_against_fake_api(tmp_path):
    """The live client end to end against a local stand-in for api.php."""
    import threading
    import urllib.parse
    from http.server import BaseHTTPRequestHandler, HTTPServer

    hits = []

    class FakeWiki(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            url = urllib.parse.urlparse(self.path)
            q = dict(urllib.parse.parse_qsl(url.query))
            hits.append(q)
            if url.path == "/robots.txt":
                body = "User-agent: ClaudeBot\nDisallow: /\n\nUser-agent: *\nAllow: /api.php\nDisallow: /wiki/Special:\n"
            elif q.get("list") == "categorymembers":
                if q.get("cmtitle") != "Category:Characters":
                    body = json.dumps({"query": {"categorymembers": []}})
                elif "cmcontinue" not in q:
                    body = json.dumps({"query": {"categorymembers": [{"title": "Barf"}]},
                                       "continue": {"cmcontinue": "next", "continue": "-||"}})
                else:
                    body = json.dumps({"query": {"categorymembers": [{"title": "Lone Starr"}]}})
            elif q.get("prop") == "revisions|categories":
                pages = [{"title": "Barf", "revisions": [{"slots": {"main": {"content": BARF_WIKITEXT}}}],
                          "categories": [{"title": "Category:Characters"}]},
                         {"title": "Lone Starr", "missing": True}]
                body = json.dumps({"query": {"pages": pages}})
            else:
                body = json.dumps({"query": {"rightsinfo": {"text": "CC BY-SA", "url": "u"},
                                             "general": {"sitename": "Spaceballs Wiki"}}})
            self.send_response(200)
            self.end_headers()
            self.wfile.write(body.encode())

    server = HTTPServer(("127.0.0.1", 0), FakeWiki)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        client = wiki.WikiClient(base, cache_dir=tmp_path / "cache", delay=0)
        assert client.license()["sitename"] == "Spaceballs Wiki"
        assert client.category_members("Characters") == ["Barf", "Lone Starr"]
        pages = list(client.pages(["Barf", "Lone Starr"]))
        assert [p.title for p in pages] == ["Barf"] and pages[0].categories == ["Characters"]

        api_hits = len([h for h in hits if h])
        list(client.pages(["Barf", "Lone Starr"]))           # served from the disk cache
        assert len([h for h in hits if h]) == api_hits

        with pytest.raises(wiki.RobotsDisallowed):
            wiki.WikiClient(base, cache_dir=tmp_path / "c2", delay=0,
                            user_agent="ClaudeBot").license()
    finally:
        server.shutdown()


def test_forbidden_robots_txt_stops_the_scrape(tmp_path):
    import threading
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class Forbidden(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            self.send_response(403)
            self.end_headers()

    server = HTTPServer(("127.0.0.1", 0), Forbidden)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        client = wiki.WikiClient(f"http://127.0.0.1:{server.server_port}",
                                 cache_dir=tmp_path / "cache", delay=0)
        with pytest.raises(wiki.RobotsDisallowed, match="dump"):
            client.license()
    finally:
        server.shutdown()
