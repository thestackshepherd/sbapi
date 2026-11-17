# sbapi

Spaceballs API (SBAPI) — a REST API for data from the 1987 film *Spaceballs*
(characters, planets, vehicles, quotes, and more).

**Status:** early scaffolding. The Flask app, Postgres schema, and
SQLAlchemy models are in place. Only `GET /api/health` and `GET /api/characters`
are implemented; the other resources don't have routes yet.

## Stack

- Python 3.15, managed with [uv](https://docs.astral.sh/uv/)
- Flask + Gunicorn, behind an nginx reverse proxy
- PostgreSQL, accessed via SQLAlchemy + psycopg
- Docker / Docker Compose for local dev
- Terraform boilerplate for AWS deployment (see `src/sbapi/infra/`)

## Project layout

```
src/sbapi/
  app/
    main.py                    # Flask app factory
    wsgi.py                    # Gunicorn entry point
    database/
      connection.py            # SQLAlchemy engine setup
      sbapi_devdb_schema.sql   # dev schema: drops and recreates every table
      sbapi_prod_schema.sql    # production schema
      sbapidb_rebase.sql       # wipes the public schema entirely
    models/                    # SQLAlchemy models
    repositories/              # database queries used by the routes
    routes/                    # Flask blueprints (in progress)
    scripts/                   # populate scripts (database_populate_*.py)
  infra/                  # Terraform for AWS (state backend + bootstrap)
    local/
      nginx/nginx.conf     # local reverse proxy: / -> web/, /api/ -> app replicas
      web/index.html       # placeholder frontend served at /
Dockerfile
sbapi-compose.yaml        # local Postgres + app replicas + nginx proxy
```

## Local development

```sh
cp .envexample .env   # fill in DB credentials if you want non-default values
uv sync
docker compose -f sbapi-compose.yaml up
```

This starts a Postgres container, three replicas of the Flask app (via
Gunicorn, on port 8080 inside the container; set `APP_REPLICAS` to change the
count) and an nginx proxy published on host port 8080 (`PROXY_HOST_PORT`). The
proxy serves the placeholder frontend at `/` and load-balances `/api/` across
the app replicas; the app containers publish no host ports. On first start with an empty volume, Postgres loads
`src/sbapi/app/database/sbapi_devdb_schema.sql` automatically. That file drops
and recreates every table, so after changing it you can re-run it against the
running database instead of resetting the volume (this deletes all table data):

```sh
docker compose -f sbapi-compose.yaml exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
  < src/sbapi/app/database/sbapi_devdb_schema.sql
```

To start from a completely empty database, use
`docker compose -f sbapi-compose.yaml down -v`.

Check it is up (the app container also has a healthcheck on this):

```sh
curl localhost:8080/api/health        # {"status":"ok"} once the DB is reachable
curl localhost:8080/api/characters    # [] until data is loaded
```

Postgres is published on `127.0.0.1` only, at `DB_HOST_PORT` (default 5432).
If port 5432 is already taken locally, set `DB_HOST_PORT` in `.env` (and
`DATABASE_PORT` to match when running the populate scripts from your machine).

## Loading data

Data comes from the film itself (its credits and script) and reference sites such
as the [Spaceballs Wiki](https://spaceballs.fandom.com) (CC BY-SA 3.0). Values
that can't be sourced are left null, never guessed.

The tables are filled by `src/sbapi/app/scripts/database_populate_main.py`,
installed as a console command. The data it inserts lives in the sibling
`database_populate_<table>.py` modules: `planets`, `actors`, `characters`,
`vehicles`, `items`, `quotes`, `character_actors`, `vehicle_crew`, `trivia`,
and `citations`. Link and annotation rows (character_actors, vehicle_crew,
trivia, citations, item owners, quote speakers) name the rows they point at
(e.g. `"character_name": "Lone Starr"`), and the ids are looked up when the
row is inserted. Run it from the repo root so `.env` is found:

```sh
uv run populate   # inserts planets, actors, characters, vehicles, items, quotes,
                  # character_actors, vehicle_crew, trivia, and citations
```

The tables must already exist (see [Local development](#local-development)).
`populate` runs on your machine and connects to the database directly over the
loopback port (`DATABASE_HOST=localhost`, `DATABASE_PORT` = `DB_HOST_PORT`),
not through the proxy.
The scripts are safe to re-run: a row whose name is already in the table is
skipped, not duplicated or updated. Link rows are skipped when the same pair
already exists, trivia and citations when the same text is already attached to
the same row, and a row whose referenced character, actor, vehicle, or item
is missing is skipped with a printed warning.

Tests: `uv run pytest`.

## Deployment

Terraform boilerplate for AWS lives in `src/sbapi/infra/` — see that
directory's README for the state-backend bootstrap and usage. Container
registry (ECR) and compute resources aren't defined yet.
