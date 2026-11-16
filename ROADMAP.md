# SBAPI Roadmap

First pass, written 2026-11-16 from `main` @ `4e077a5`. It is a proposal to
discuss, not a commitment. Issue numbers refer to
[thestackshepherd/sbapi](https://github.com/thestackshepherd/sbapi/issues).

## Where we are today

What works, verified locally on `main`:

- **Local stack.** `docker compose -f sbapi-compose.yaml up` runs Postgres 18,
  3 Gunicorn replicas of the Flask app, and an nginx proxy on `:8080`
  (`sbapi-compose.yaml`, `src/sbapi/infra/local/nginx/nginx.conf`). The API is
  served under `/api` by the app itself (`src/sbapi/app/main.py`).
- **Endpoints.** Only `GET /api/health` (runs `SELECT 1`) and
  `GET /api/characters` (every row, no paging or filters) exist
  (`src/sbapi/app/routes/sbapi_flask_route_characters.py`,
  `src/sbapi/app/repositories/sbapi_sqlalchemy_repo_characters.py`).
- **Schema and models.** There are 10 tables in
  `src/sbapi/app/database/sbapi_devdb_schema.sql`, plus one SQLAlchemy model per
  table in `src/sbapi/app/models/`. I built one database from the SQL file and
  one from `Base.metadata.create_all`. Their `pg_dump -s` output is
  **identical**, so the models already match the schema (#3).
- **Data.** `uv run populate` fills planets, actors and characters
  (`src/sbapi/app/scripts/`). PR #14 (open) adds vehicles, items, quotes,
  character_actors, vehicle_crew, trivia and citations.
- **Tests and CI.** `tests/test_api_prefix.py` has 3 tests that check route
  registration only. `.github/workflows/build-and-deploy.yaml` only checks out
  the code. It runs no tests, lint or build. SonarCloud runs on PRs.
- **Infra.** `src/sbapi/infra/bootstrap/` defines the S3 state bucket and the
  DynamoDB lock table. The main config (`src/sbapi/infra/main.tf`) is empty:
  no ECR, compute, database or networking yet.

## What's missing for a first production deploy

1. A schema-management path for prod. `sbapi_prod_schema.sql` is a copy of the
   dev file and starts every table with `DROP TABLE IF EXISTS ... CASCADE`.
   That is unsafe to run against a live database (#12).
2. Read endpoints for the other 9 tables, plus detail (`/<id>`) routes, paging
   and JSON error responses. Today a 404 or a DB outage returns Flask's HTML
   error page.
3. CI that actually gates merges: lint, tests against a real Postgres, and a
   Docker build.
4. AWS resources: a container registry, compute, managed Postgres, networking
   and secrets (#4), plus a pipeline that builds, pushes and deploys (#5).
5. A seeded prod database. Decide whether prod is seeded by `populate` or by a
   data migration.

## Suggested order

| # | Milestone | Issues | Done when |
|---|-----------|--------|-----------|
| 1 | Finish dev data | PR #14 | all 10 tables populated by `uv run populate` |
| 2 | Close out models | #3 | lint clean (`ruff --select F` shows 16 F821s, from forward refs without `TYPE_CHECKING` imports); a test asserts models == schema; close #3 |
| 3 | CI that runs checks | new (see drafts) | ruff + pytest (with a Postgres service) + `docker build` on every PR |
| 4 | Alembic baseline | #12 | baseline revision equals the current schema; `alembic upgrade head` on an empty DB matches `create_all`; prod no longer uses a DROP script |
| 5 | ERD | #1 | Mermaid ERD generated from `Base.metadata` (or the migrated DB); CI fails if it is stale |
| 6 | Read API for all tables | new | list + detail + paging for each table, JSON errors, tests per route |
| 7 | Terraform for prod | #4 | `terraform plan` is clean for ECR + compute + RDS + secrets; nothing applied until Jaden signs off |
| 8 | Build and deploy | #5 | on merge to `main`: test, build, push the image, run migrations, deploy |

Steps 2 and 3 are small and unblock everything else. Doing #12 before #4/#5
means the deploy pipeline can run `alembic upgrade head` instead of SQL files.

## Tech debt

- `src/sbapi/app/database/connection.py` hardcodes `postgresql+psycopg` and
  ignores `DATABASE_DRIVER`, which `.envexample` and the compose file both set.
- Three overlapping SQL files: `sbapi_devdb_schema.sql`,
  `sbapi_prod_schema.sql` (identical apart from one comment) and
  `sbapidb_rebase.sql`. There is also a root-level `sbapidatabase.session.sql`
  with the same content as the rebase file.
- The schema uses `CREATE INDEX CONCURRENTLY`, which fails inside a transaction
  (I checked with `psql -1`). Alembic runs migrations in a transaction, so the
  baseline can't copy the SQL verbatim. On empty tables a plain `CREATE INDEX`
  is fine.
- `idx_actors` duplicates the index that `UNIQUE (actor_name)` already creates.
- `planets.ruler_id` is free text (`"skroob"`), not a foreign key to
  `characters`.
- Mixed `Optional[X]` / `X | None` and quoted/unquoted annotations across the
  models. `populate_actors` is the only populate function that doesn't print
  added/skipped.
- No ruff, mypy or pytest config in `pyproject.toml`. ruff and mypy aren't in
  the `dev` group.
- Docker: the image runs as root and `pip install uv` is unpinned. The
  container's Gunicorn uses its default of 1 worker, because `SBAPI_WORKERS` is
  only read by the `sbapi` console script (`wsgi.py:main`).
- The workflow uses `actions/checkout@v3` (Node 20 deprecation warnings).

## Testing gaps

- No test touches a database: none for the repositories, the populate scripts
  or `/api/health` with the DB up or down.
- No test checks that the models match the SQL schema (or the migrations).
- No response-shape tests for `/api/characters`.
- Tests don't run in CI.
- `tests/test_api_prefix.py` needs fake `DATABASE_*` env vars just to build the
  app. A shared `conftest.py` fixture (and, later, a Postgres fixture) would
  remove the copy-paste once there are more test files.
