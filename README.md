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
- Terraform boilerplate for AWS deployment (see `sbapi_tf/`)

## Project layout

```
sbapi_api/                       # Flask backend (uv workspace member)
  src/sbapi_api/
    main.py                      # Flask app factory
    wsgi.py                      # Gunicorn entry point
    database/connection.py       # SQLAlchemy engine setup
    models/                      # SQLAlchemy models
    repositories/  routes/       # data access, Flask blueprints (in progress)
    dtos/  services/             # placeholders
  tests/
sbapi_scripts/                   # db + data tooling (uv workspace member)
  src/sbapi_scripts/
    db/schema.sql                # Postgres schema (tables, indexes)
    ingest/                      # wiki -> JSON -> Postgres data pipeline
    generate_erd.py              # schema.sql -> docs/ERD.md
  tests/
sbapi_ui/                        # placeholder for the future Angular front end
sbapi_tf/                        # Terraform for AWS (state backend + bootstrap)
schemas/scrape/                  # JSON Schemas for wiki-scraped records
data/sample/                     # a few hand-checked records for trying the loader
docs/
Dockerfile
sbapi-compose.yaml               # local Postgres + app via Docker Compose
```

## Local development

```sh
cp .envexample .env   # fill in DB credentials if you want non-default values
uv sync --all-packages
docker compose -f sbapi-compose.yaml up
```

This starts a Postgres container and the Flask app (via Gunicorn) in
another container. On first start with an empty volume, Postgres loads
`sbapi_scripts/src/sbapi_scripts/db/schema.sql` automatically. If you change
the schema, reset with `docker compose -f sbapi-compose.yaml down -v`.

Check it is up (the app container also has a healthcheck on this):

```sh
curl localhost:8000/health        # {"status":"ok"} once the DB is reachable
curl localhost:8000/characters    # [] until data is loaded
```

If port 5432 is already taken locally, set `DB_HOST_PORT` in `.env` (and
`DATABASE_PORT` to match when running the ingest commands from your machine).

To get data in quickly, load the sourced sample records (see below):
`uv run --package sbapi_scripts --extra ingest python -m sbapi_scripts.ingest load data/sample`.

## Loading data

Data comes from the [Spaceballs Wiki](https://spaceballs.fandom.com) (CC BY-SA 3.0).
The pipeline lives in `sbapi_scripts/src/sbapi_scripts/ingest/`:

```sh
uv sync --all-packages --extra ingest
python -m sbapi_scripts.ingest scrape --limit 20   # trial run: live wiki API -> data/scrape/
python -m sbapi_scripts.ingest scrape              # everything (1 request/second, cached in .cache/wiki)
python -m sbapi_scripts.ingest validate            # check records against schemas/scrape/
python -m sbapi_scripts.ingest load                # insert into Postgres (DATABASE_* env vars)
```

- **Scrape** uses `api.php`, which the wiki's robots.txt allows for general
  bots. It checks robots.txt for its own user agent, waits between requests,
  and caches every response, so re-runs are cheap. Run it from your own
  machine: the wiki blocks Anthropic's crawler.
- `python -m sbapi_scripts.ingest dump FILE` reads a MediaWiki XML dump instead
  (download from the wiki's Special:Statistics page), with no network at all.
- Each run writes `_report.json` with the categories and infobox fields the
  wiki uses that `ingest/config.py` doesn't map yet. Tune the config from it.
- **Load** is idempotent and runs in one transaction. Names that match no
  record are left null and listed, never guessed.
- `data/sample/` holds four pages' worth of records to try the loader:
  `python -m sbapi_scripts.ingest load data/sample`.

Tests: `uv run pytest` (set `SBAPI_TEST_DSN` to include the Postgres load test).

## Deployment

Terraform boilerplate for AWS lives in `sbapi_tf/` — see that
directory's README for the state-backend bootstrap and usage. Container
registry (ECR) and compute resources aren't defined yet.
