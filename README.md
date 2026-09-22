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
another container, wired together with the env vars in `.env`.

To load the schema into the database:

```sh
psql "$DATABASE_URL" -f src/sbapi/app/database/sbapidatabase_schema.sql
```

## Deployment

Terraform boilerplate for AWS lives in `src/sbapi/infra/` — see that
directory's README for the state-backend bootstrap and usage. Container
registry (ECR) and compute resources aren't defined yet.
