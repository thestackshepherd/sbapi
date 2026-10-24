# sbapi

Spaceballs API (SBAPI) — a REST API for data from the 1987 film *Spaceballs*
(characters, locations, factions, spacecraft, quotes, and more).

**Status:** early scaffolding. The Flask app, Postgres schema, and
SQLAlchemy models are in place; the HTTP routes are still empty stubs.

## Stack

- Python 3.14, managed with [uv](https://docs.astral.sh/uv/)
- Flask + Gunicorn
- PostgreSQL, accessed via SQLAlchemy + psycopg
- Docker / Docker Compose for local dev
- Terraform boilerplate for AWS deployment (see `src/sbapi/infra/`)

## Project layout

```
src/sbapi/
  main.py                 # Flask app factory
  wsgi.py                 # Gunicorn entry point
  app/
    database/
      connection.py            # SQLAlchemy engine setup
      sbapidatabase_schema.sql # Postgres schema (tables, indexes)
    models/                    # SQLAlchemy models
    routes/                    # Flask blueprints (in progress)
  ingest/                 # wiki -> JSON -> Postgres data pipeline
schemas/scrape/           # JSON Schemas for wiki-scraped records
data/sample/              # a few hand-checked records for trying the loader
tests/
  infra/                  # Terraform for AWS (state backend + bootstrap)
Dockerfile
sbapi-compose.yaml        # local Postgres + app via Docker Compose
```

## Local development

```sh
cp .envexample .env   # fill in DB credentials if you want non-default values
uv sync
docker compose -f sbapi-compose.yaml up
```

This starts a Postgres container and the Flask app (via Gunicorn) in
another container. On first start with an empty volume, Postgres loads
`src/sbapi/app/database/sbapidatabase_schema.sql` automatically. If you change
the schema, reset with `docker compose -f sbapi-compose.yaml down -v`.

Check it is up (the app container also has a healthcheck on this):

```sh
curl localhost:8000/health        # {"status":"ok"} once the DB is reachable
curl localhost:8000/characters    # [] until data is loaded
```

If port 5432 is already taken locally, set `DB_HOST_PORT` in `.env` (and
`DATABASE_PORT` to match when running the ingest commands from your machine).

To get data in quickly, load the sourced sample records (see below):
`cd src && uv run --extra ingest python -m sbapi.ingest load ../data/sample`.

## Loading data

Data comes from the [Spaceballs Wiki](https://spaceballs.fandom.com) (CC BY-SA 3.0).
The pipeline lives in `src/sbapi/ingest/`:

```sh
uv sync --extra ingest
cd src
python -m sbapi.ingest scrape --limit 20   # trial run: live wiki API -> ../data/scrape/
python -m sbapi.ingest scrape              # everything (1 request/second, cached in .cache/wiki)
python -m sbapi.ingest validate            # check records against schemas/scrape/
python -m sbapi.ingest load                # insert into Postgres (DATABASE_* env vars)
```

- **Scrape** uses `api.php`, which the wiki's robots.txt allows for general
  bots. It checks robots.txt for its own user agent, waits between requests,
  and caches every response, so re-runs are cheap. Run it from your own
  machine: the wiki blocks Anthropic's crawler.
- `python -m sbapi.ingest dump FILE` reads a MediaWiki XML dump instead
  (download from the wiki's Special:Statistics page), with no network at all.
- Each run writes `_report.json` with the categories and infobox fields the
  wiki uses that `ingest/config.py` doesn't map yet. Tune the config from it.
- **Load** is idempotent and runs in one transaction. Names that match no
  record are left null and listed, never guessed.
- `data/sample/` holds four pages' worth of records to try the loader:
  `python -m sbapi.ingest load ../data/sample`.

Tests: `uv run pytest` (set `SBAPI_TEST_DSN` to include the Postgres load test).

## Deployment

Terraform boilerplate for AWS lives in `src/sbapi/infra/` — see that
directory's README for the state-backend bootstrap and usage. Container
registry (ECR) and compute resources aren't defined yet.
