# sbapi

Spaceballs API (SBAPI) — a REST API for data from the 1987 film *Spaceballs*
(characters, locations, factions, spacecraft, quotes, and more).

**Status:** early scaffolding. The Flask app, Postgres schema, and
SQLAlchemy models are in place; the HTTP routes are still empty stubs.

## Stack

- Python 3.15, managed with [uv](https://docs.astral.sh/uv/)
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
      sbapi_devdb_schema.sql   # dev schema: drops and recreates every table
      sbapidb_rebase.sql       # wipes the public schema entirely
    models/                    # SQLAlchemy models
    routes/                    # Flask blueprints (in progress)
    scripts/                   # populate scripts (e.g. database_populate_actors.py)
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
curl localhost:8000/health        # {"status":"ok"} once the DB is reachable
curl localhost:8000/characters    # [] until data is loaded
```

If port 5432 is already taken locally, set `DB_HOST_PORT` in `.env` (and
`DATABASE_PORT` to match when running the populate scripts from your machine).

## Loading data

Data comes from the film itself (its credits and script) and reference sites such
as the [Spaceballs Wiki](https://spaceballs.fandom.com) (CC BY-SA 3.0). Values
that can't be sourced are left null, never guessed.

Each table is filled by a script in `src/sbapi/app/scripts/`, installed as a
console command. Run them from the repo root so `.env` is found:

```sh
uv run populate_actors   # inserts the cast into the actors table
```

Tests: `uv run pytest`.

## Deployment

Terraform boilerplate for AWS lives in `src/sbapi/infra/` — see that
directory's README for the state-backend bootstrap and usage. Container
registry (ECR) and compute resources aren't defined yet.
