# Package restructure (uv workspace) — design

## Intent
Organize the repo into four self-contained top-level packages so the API, the
db/data tooling, the future UI and the infrastructure each have a clear home.
This is an organization-only change: moves and renames, no behavior changes.

Said by the owner: packages `sbapi_api`, `sbapi_scripts`, `sbapi_ui`, `sbapi_tf`;
each its own package with `__init__.py` where Python; follow the uv standard;
`sbapi_ui` stays a placeholder (Angular later); db scripts live in `sbapi_scripts`.

Assumptions: "uv standard" = uv workspace with `<member>/src/<member>/` layout;
the UI and Terraform are not Python, so they get no `__init__.py`.

## Success criteria
- `uv sync --all-packages` works; `uv run pytest` passes in both Python packages.
- `docker compose up --build` gives a healthy stack; `/health` and `/characters`
  work and the sample data loads.
- `python -m sbapi_scripts.ingest validate` works.
- No stale references to `src/sbapi`, `sbapi.app` or `sbapi.ingest` remain.

## Layout
```
pyproject.toml            # workspace root only: members = [sbapi_api, sbapi_scripts]; dev group (pytest)
uv.lock                   # single lockfile
sbapi_api/                # Flask backend
  pyproject.toml          # flask, gunicorn, sqlalchemy, psycopg[binary], dotenv; script `sbapi`
  src/sbapi_api/          # __init__, main, wsgi, database/connection, models, repositories, routes, dtos, services
  tests/                  # replaces the empty src/sbapi/test/* stubs
sbapi_scripts/            # db + data tooling
  pyproject.toml          # psycopg[binary]; extra `ingest`: jsonschema, mwparserfromhell
  src/sbapi_scripts/
    db/schema.sql         # schema is owned here
    ingest/               # scraper/loader, moved as-is
    generate_erd.py
  tests/test_ingest.py
sbapi_ui/README.md        # placeholder only
sbapi_tf/                 # Terraform, moved from src/sbapi/infra
schemas/scrape/           # stays at root (shared contracts)
Dockerfile, sbapi-compose.yaml, README.md, docs/, .github/
```

The two Python packages do not import each other: ingest uses raw psycopg SQL.
The schema SQL is their only shared contract.

## Mechanics
- All moves use `git mv`; imports renamed `sbapi.app.*` -> `sbapi_api.*`,
  `sbapi.ingest.*` -> `sbapi_scripts.ingest.*`.
- Dockerfile builds only the API: `uv sync --frozen --package sbapi_api --no-dev`;
  gunicorn target `sbapi_api.wsgi:app`. The scraper's dependencies stay out of the image.
- Compose mounts `sbapi_scripts/src/sbapi_scripts/db/schema.sql` into initdb.
- Update path references: README, CI workflow (verify it), `docs/ERD.md` header and
  generator defaults, `.gitignore`, `cspell.json`, Terraform README, test schema path.
- The empty `dtos/` and `services/` dirs become real packages with `__init__.py`.

## Out of scope
New routes, behavior changes, Angular scaffolding, Terraform changes beyond the move.

## Verification
Run the success criteria above after the move; finish with a grep for stale paths.

## Risks
- Hatch/uv_build module-name rules: member names are `sbapi_api` / `sbapi_scripts`
  (valid module names), so the `src/<name>` layout needs no overrides.
- The Docker build must see the whole workspace (root `pyproject.toml` + member
  `pyproject.toml` files) even though it installs only one member.
