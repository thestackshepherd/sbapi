# Package Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the repo into a uv workspace of four top-level packages (`sbapi_api`, `sbapi_scripts`, `sbapi_ui`, `sbapi_tf`) with no behavior change.

**Architecture:** Root `pyproject.toml` is a workspace root only; `sbapi_api` and `sbapi_scripts` are members using the `<member>/src/<member>/` layout and do not import each other (schema SQL is their only shared contract). `sbapi_ui` is a README placeholder; `sbapi_tf` is the moved Terraform.

**Tech Stack:** uv workspaces, uv_build, Flask, SQLAlchemy, psycopg, pytest, Docker Compose, Terraform.

**Spec:** `docs/superpowers/specs/2026-10-24-package-restructure-design.md`

## Global Constraints

- All moves use `git mv`; imports `sbapi.app.*` -> `sbapi_api.*`, `sbapi.ingest.*` -> `sbapi_scripts.ingest.*`.
- Organization only: no new routes, no behavior changes, no Angular scaffolding, no Terraform edits beyond the move.
- `requires-python = ">=3.14"`, build backend `uv_build>=0.12.3,<0.13.0` (as today).
- Dependencies as today: api = flask, gunicorn, sqlalchemy, `psycopg[binary]`, dotenv; scripts = `psycopg[binary]`, extra `ingest` = jsonschema, mwparserfromhell; dev group (pytest) stays at the workspace root.
- Console script `sbapi` is kept, pointing at `sbapi_api.wsgi:main`.
- Data integrity (CLAUDE.md): do not touch `data/sample` content.
- Work on branch `restructure-packages`.

## Review Focus

- `validate.py` locates `schemas/scrape` with `Path(__file__).resolve().parents[3]`; after the move the repo root is `parents[4]`. Wrong depth silently breaks `validate`/`load`. Pinned in Task 2.
- Docker image must still start and pass `/health` while installing only `sbapi_api` (no `jsonschema`/`mwparserfromhell`). Pinned in Task 4.
- Fresh Postgres volume must still auto-load the schema from its new path (a stale compose mount creates an empty DB). Pinned in Task 4.
- A package that is empty on disk but listed as a member (`dtos`, `services`) must still import. Pinned in Task 1.
- Stale references in docs/CI/cspell give wrong instructions without failing anything. Pinned by the grep in Task 4.

---

### Task 1: Workspace root and `sbapi_api`

**Files:**
- Modify: `pyproject.toml` (becomes workspace root)
- Create: `sbapi_api/pyproject.toml`, `sbapi_api/src/sbapi_api/dtos/__init__.py`, `sbapi_api/src/sbapi_api/services/__init__.py`, `sbapi_api/tests/test_app.py`
- Move: `src/sbapi/app/*` -> `sbapi_api/src/sbapi_api/` (includes `__init__.py`, `main.py`, `wsgi.py`, `database/connection.py`, `models/`, `repositories/`, `routes/`); delete `src/sbapi/__init__.py`, `src/sbapi/test/*` stubs
- Add `__init__.py` to `routes/`, `repositories/`, `database/` if missing

**Interfaces:**
- Produces: importable `sbapi_api.main.create_app() -> Flask`, `sbapi_api.wsgi:app`, `sbapi_api.wsgi:main`.

- [ ] **Step 1: Write the failing test** `sbapi_api/tests/test_app.py`: `test_create_app_registers_health_and_characters` builds `create_app()` and asserts the URL map contains `/health` and `/characters`; `test_empty_subpackages_import` imports `sbapi_api.dtos` and `sbapi_api.services`.
- [ ] **Step 2: Run** `uv run --package sbapi_api pytest sbapi_api/tests -v`. Expected: FAIL (no package yet).
- [ ] **Step 3: Move and rename.** `git mv` the app tree as listed; rewrite every `sbapi.app.` import to `sbapi_api.` (use a sed-free approach on macOS: `python3` or Edit; plain `sed -i` needs `-i ''`). Add the two empty-package `__init__.py` files.
- [ ] **Step 4: Packaging.** Write `sbapi_api/pyproject.toml` (name `sbapi-api`, deps and script from Global Constraints, `uv_build` backend). Reduce root `pyproject.toml` to project metadata plus `[tool.uv.workspace] members = ["sbapi_api", "sbapi_scripts"]` and `[dependency-groups] dev = ["pytest>=8.3"]`. Create a stub `sbapi_scripts/pyproject.toml` only if `uv lock` requires the member to exist (finish it in Task 2).
- [ ] **Step 5: Run** `uv lock && uv sync --all-packages && uv run pytest sbapi_api/tests -v`. Expected: PASS.
- [ ] **Step 6: Commit** `git commit -m "Move API into sbapi_api workspace package"`.

### Task 2: `sbapi_scripts`

**Files:**
- Create: `sbapi_scripts/pyproject.toml`, `sbapi_scripts/src/sbapi_scripts/__init__.py`, `sbapi_scripts/src/sbapi_scripts/db/__init__.py`
- Move: `src/sbapi/ingest/` -> `sbapi_scripts/src/sbapi_scripts/ingest/`; `src/sbapi/app/database/sbapidatabase_schema.sql` -> `sbapi_scripts/src/sbapi_scripts/db/schema.sql`; `scripts/generate_erd.py` -> `sbapi_scripts/src/sbapi_scripts/generate_erd.py`; `tests/test_ingest.py` -> `sbapi_scripts/tests/test_ingest.py`
- Modify: `ingest/validate.py:12`, `generate_erd.py` (`REPO_ROOT`, `DEFAULT_SCHEMA`, usage text), `tests/test_ingest.py` (imports, `ROOT`, schema path), ingest docstrings/help text (`python -m sbapi.ingest` -> `python -m sbapi_scripts.ingest`)

**Interfaces:**
- Produces: `python -m sbapi_scripts.ingest {scrape,dump,validate,load,report}`; schema at `sbapi_scripts/src/sbapi_scripts/db/schema.sql`.

- [ ] **Step 1: Write the failing test** in `sbapi_scripts/tests/test_ingest.py`: update imports to `sbapi_scripts.ingest`; add `test_schema_dir_points_at_repo_schemas` asserting `validate.SCHEMA_DIR.is_dir()` and that `SCHEMA_DIR / "character.schema.json"` exists.
- [ ] **Step 2: Run** `uv run --package sbapi_scripts --extra ingest pytest sbapi_scripts/tests -v`. Expected: FAIL (import error).
- [ ] **Step 3: Move and fix paths.** `git mv` as listed. In `validate.py` change `parents[3]` to `parents[4]`. In `generate_erd.py` set `REPO_ROOT` to the repo root (`parents[3]` from its new location) and `DEFAULT_SCHEMA` to the new `db/schema.sql` path; fix the test's `ROOT` (`parents[2]`) and schema path.
- [ ] **Step 4: Packaging.** Write `sbapi_scripts/pyproject.toml` per Global Constraints.
- [ ] **Step 5: Run** the tests from Step 2 plus `uv run --package sbapi_scripts --extra ingest python -m sbapi_scripts.ingest validate data/sample` and `uv run python -m sbapi_scripts.generate_erd` (then `git diff docs/ERD.md` should show at most the header line). Expected: tests PASS (Postgres test skipped), validate succeeds, ERD unchanged apart from the header.
- [ ] **Step 6: Commit** `git commit -m "Move db and ingest tooling into sbapi_scripts"`.

### Task 3: `sbapi_tf` and `sbapi_ui`

**Files:**
- Move: `src/sbapi/infra/` -> `sbapi_tf/` (contents at top level, including `bootstrap/` and its hidden `.gitignore`)
- Create: `sbapi_ui/README.md` (one paragraph: placeholder for the future Angular app)
- Delete: now-empty `src/` tree

- [ ] **Step 1: Move** with `git mv src/sbapi/infra sbapi_tf`; create the README; confirm `git ls-files src` is empty.
- [ ] **Step 2: Verify** `ls -a sbapi_tf` shows `.gitignore`, `bootstrap/`, `backend.hcl.example`; relative `source` paths in `sbapi_tf/*.tf` (if any) still resolve (grep for `source =`/`../`).
- [ ] **Step 3: Commit** `git commit -m "Add sbapi_tf and sbapi_ui placeholder packages"`.

### Task 4: Docker, compose, CI, docs, end-to-end

**Files:**
- Modify: `Dockerfile`, `sbapi-compose.yaml:14`, `.dockerignore`, `README.md`, `schemas/scrape/README.md:13`, `docs/ERD.md:3` (regenerated), `data/sample/ATTRIBUTION.md:10`, `.github/workflows/build-and-deploy.yaml` (check for path use), `cspell.json`, `.gitignore`, `sbapi_tf/README.md`

- [ ] **Step 1: Dockerfile.** Copy root `pyproject.toml`, `uv.lock`, `.python-version`, and both member `pyproject.toml` files; `uv sync --frozen --package sbapi_api --no-dev --no-install-project`; copy `sbapi_api/` and `README.md`; sync again; `CMD` target `sbapi_api.wsgi:app`.
- [ ] **Step 2: Compose** mount `./sbapi_scripts/src/sbapi_scripts/db/schema.sql:/docker-entrypoint-initdb.d/01-schema.sql:ro`.
- [ ] **Step 3: Docs/refs.** Update the README layout tree and every command (`python -m sbapi_scripts.ingest …`, `uv sync --all-packages`, run-from-root instead of `cd src`), schema path mentions, and tf path mentions. Then run `grep -rnE "src/sbapi|sbapi\.(app|ingest)|sbapidatabase_schema|scripts/generate_erd" . --exclude-dir=.git --exclude-dir=.venv --exclude-dir=.idea --exclude=uv.lock --exclude-dir=superpowers`. Expected: no output.
- [ ] **Step 4: End-to-end.** `docker info` must succeed first. Then `DB_HOST_PORT=5433 docker compose -f sbapi-compose.yaml down -v && DB_HOST_PORT=5433 docker compose -f sbapi-compose.yaml up --build -d --wait`; `curl -s localhost:8000/health` returns `{"status":"ok"}`; `curl -s localhost:8000/characters` returns `[]`; `docker compose -f sbapi-compose.yaml exec app python -c "import jsonschema"` fails (scraper deps stay out of the image); `DATABASE_HOST=localhost DATABASE_PORT=5433 uv run --package sbapi_scripts --extra ingest python -m sbapi_scripts.ingest load data/sample` loads 2 characters, 1 media, 2 quotes, 1 vehicle; `/characters` then returns Barf and Lone Starr. Run `docker compose … down`.
- [ ] **Step 5: Full tests** `uv run --all-packages --extra ingest pytest -q`. Expected: all pass, Postgres test skipped.
- [ ] **Step 6: Commit** `git commit -m "Update Docker, compose, CI and docs for workspace layout"`.

## Self-Review Notes

Spec coverage: layout (Tasks 1-3), mechanics incl. Docker/compose/refs (Task 4), success criteria (Task 4 steps 3-5), risks (member naming in Task 1 step 4; workspace-visible Docker build in Task 4 step 1).
