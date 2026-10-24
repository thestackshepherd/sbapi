"""
Ingest pipeline: Spaceballs wiki -> scrape JSON -> Postgres.

    source (wiki.py)  : page wikitext, from the live MediaWiki API or an XML dump
    extract.py        : wikitext -> one JSON record per page (schemas/scrape/)
    validate.py       : records -> checked against the JSON Schemas
    load.py           : records -> Postgres, idempotently

Run with `python -m sbapi.ingest --help`.
"""
