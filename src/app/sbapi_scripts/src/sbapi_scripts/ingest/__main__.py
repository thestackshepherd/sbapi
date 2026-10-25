"""
CLI for the ingest pipeline.

    python -m sbapi_scripts.ingest scrape   [--out data/scrape]    live wiki API -> JSON files
    python -m sbapi_scripts.ingest dump FILE [--out data/scrape]   XML dump -> JSON files
    python -m sbapi_scripts.ingest validate [DIR]                  check JSON files against schemas
    python -m sbapi_scripts.ingest load     [DIR]                  JSON files -> Postgres (DATABASE_* env)
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from . import wiki
from . import config
from . import extract
from . import validate

ATTRIBUTION = """# Attribution

Records in this folder were extracted from **{sitename}** ({base_url}).
Its text is licensed under **{license}** ({license_url}).

Each record's `source_url` links the page it came from; that page's history
lists its authors. Changes made here: wikitext was reduced to the fields in
`schemas/scrape/`, with markup stripped. Data derived from these records
carries the same license.

Extracted {when} from {origin}.
"""


def _slug(text):
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")[:120] or "page"


def _write_records(pages, out, base_url, license_info, origin):
    out = Path(out)
    stats = {"categories": Counter(), "unmapped_fields": Counter(), "skipped": 0, "invalid": []}
    written = Counter()
    for page in pages:
        stats["categories"].update(page.categories)
        record, etype, quotes, unmapped = extract.extract(page, base_url)
        stats["unmapped_fields"].update(f"{etype}:{k}" for k in unmapped)
        if record is None:
            stats["skipped"] += 1
        items = ([(etype, record, _slug(page.title))] if record else []) + \
                [("quote", q, f"{_slug(page.title)}__{i + 1}") for i, q in enumerate(quotes)]
        for t, rec, slug in items:
            problems = validate.errors(t, rec)
            if problems:
                stats["invalid"].append({"page": page.title, "type": t, "errors": problems})
                continue
            path = out / t / f"{slug}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
            written[t] += 1

    out.mkdir(parents=True, exist_ok=True)
    (out / "ATTRIBUTION.md").write_text(ATTRIBUTION.format(
        **license_info, base_url=base_url, origin=origin,
        when=datetime.now(timezone.utc).strftime("%Y-%m-%d")))
    report = {"written": dict(written), "skipped_pages": stats["skipped"],
              "invalid": stats["invalid"],
              "unmapped_infobox_fields": dict(stats["unmapped_fields"].most_common()),
              "categories_seen": dict(stats["categories"].most_common())}
    (out / "_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"written: {dict(written)}  skipped: {stats['skipped']}  invalid: {len(stats['invalid'])}")
    print(f"report: {out / '_report.json'}  (tune sbapi/ingest/config.py from it)")


def cmd_scrape(args):
    client = wiki.WikiClient(args.wiki, cache_dir=args.cache, delay=args.delay)
    info = client.license()
    license_info = {"sitename": info["sitename"], "license": info["license"].get("text"),
                    "license_url": info["license"].get("url")}
    titles = []
    for cat, _ in config.CATEGORY_TYPES:
        members = client.category_members(cat)
        print(f"Category:{cat}: {len(members)} pages", file=sys.stderr)
        titles += members
    titles = list(dict.fromkeys(titles))[: args.limit or None]
    _write_records(client.pages(titles), args.out, args.wiki, license_info, f"{args.wiki}/api.php")


def cmd_dump(args):
    license_info = {"sitename": "Spaceballs Wiki", "license": args.license,
                    "license_url": args.license_url}
    pages = wiki.read_dump(args.file)
    if args.limit:
        pages = (p for i, p in zip(range(args.limit), pages))
    _write_records(pages, args.out, args.wiki, license_info, f"XML dump {Path(args.file).name}")


def read_records(directory):
    records = {}
    for etype in validate.ENTITY_TYPES:
        for path in sorted(Path(directory, etype).glob("*.json")):
            records.setdefault(etype, []).append(json.loads(path.read_text()))
    return records


def cmd_validate(args):
    bad = 0
    for etype, recs in read_records(args.dir).items():
        for rec in recs:
            for problem in validate.errors(etype, rec):
                bad += 1
                print(f"{etype} {rec.get('source_url')}: {problem}")
        print(f"{etype}: {len(recs)} records")
    sys.exit(1 if bad else 0)


def cmd_load(args):
    from . import load
    dsn = args.dsn or "postgresql://{u}:{p}@{h}:{port}/{db}".format(
        u=os.getenv("DATABASE_USERNAME", "postgres"), p=os.getenv("DATABASE_PASSWORD", "postgres"),
        h=os.getenv("DATABASE_HOST", "localhost"), port=os.getenv("DATABASE_PORT", "5432"),
        db=os.getenv("DATABASE_NAME", "sbapi_dev_db"))
    records = read_records(args.dir)
    invalid = [(t, r["source_url"]) for t, rs in records.items() for r in rs if validate.errors(t, r)]
    if invalid:
        sys.exit(f"refusing to load, invalid records: {invalid} (run `validate`)")
    print("loaded:\n" + load.load(dsn, records).summary())


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m sbapi_scripts.ingest", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("scrape", help="fetch pages from the live wiki API")
    p.add_argument("--wiki", default=wiki.DEFAULT_WIKI)
    p.add_argument("--out", default="data/scrape")
    p.add_argument("--cache", default=".cache/wiki")
    p.add_argument("--delay", type=float, default=1.0, help="seconds between requests")
    p.add_argument("--limit", type=int, help="stop after N pages (for a trial run)")
    p.set_defaults(func=cmd_scrape)

    p = sub.add_parser("dump", help="read pages from a MediaWiki XML dump")
    p.add_argument("file")
    p.add_argument("--wiki", default=wiki.DEFAULT_WIKI, help="base URL for source_url links")
    p.add_argument("--out", default="data/scrape")
    p.add_argument("--license", default="CC BY-SA 3.0")
    p.add_argument("--license-url", default="https://creativecommons.org/licenses/by-sa/3.0/")
    p.add_argument("--limit", type=int)
    p.set_defaults(func=cmd_dump)

    p = sub.add_parser("validate", help="check JSON files against schemas/scrape/")
    p.add_argument("dir", nargs="?", default="data/scrape")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("load", help="insert JSON files into Postgres, idempotently")
    p.add_argument("dir", nargs="?", default="data/scrape")
    p.add_argument("--dsn", help="defaults to DATABASE_* environment variables")
    p.set_defaults(func=cmd_load)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
