# Local Infra Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run the API as 3 Gunicorn replicas behind a single nginx entry point locally, with the API under `/api` and a placeholder frontend at `/`.

**Architecture:** The Flask app serves everything under an `/api` prefix (in the app, not an nginx rewrite) so it behaves the same behind nginx or a future ALB. Docker Compose runs `proxy` (nginx, the only published port), `app` (replicated, unpublished) and `db`. nginx round-robins across replicas via Docker DNS and serves a static placeholder at `/`.

**Tech Stack:** Flask, Gunicorn, nginx:alpine, Docker Compose, pytest (via `uv run pytest`).

**Spec:** `docs/superpowers/specs/2026-11-15-local-infra-design.md`

## Global Constraints

- Proxy is `nginx:alpine`. No HAProxy, TLS, Redis, metrics, CORS or Terraform/AWS work.
- Only `proxy` publishes a port to the host: `${PROXY_HOST_PORT:-8080}:80`.
- `app` runs `deploy.replicas: 3`, publishes no host port, listens on 8080 in the container.
- `db` host port binds to `127.0.0.1` only (`127.0.0.1:${DB_HOST_PORT:-5432}:5432`).
- API routes become `/api/characters` and `/api/health`. The prefix lives in Flask.
- nginx files live in `src/sbapi/infra/local/` (`nginx/nginx.conf`, `web/index.html`).
- The nginx access log includes `$upstream_addr`.
- Gunicorn stays on sync workers; Dockerfile CMD is already 8080 and needs no change.
- Do not commit unless the user asks.

## Review Focus

Failure modes the spec implies but doesn't spell out, most likely first:

1. Old unprefixed paths (`/health`, `/characters`) must not serve API data. Pinned in Task 1.
2. A replica restarting gets a new IP; nginx must keep routing instead of caching the stale address. Pinned in Task 3.
3. An unknown path under `/api/` must reach Flask (JSON/Flask 404), not fall through to the placeholder page. Pinned in Task 3.
4. With Postgres down, `/api/health` must fail fast with a 5xx through nginx, not hang. Pinned in Task 3.
5. `uv run populate` must still reach Postgres through the loopback port. Pinned in Task 3.

---

### Task 1: Move the API under `/api`

**Files:**
- Modify: `src/sbapi/app/routes/sbapi_flask_route_characters.py` (blueprint `url_prefix`)
- Modify: `src/sbapi/app/main.py` (health route)
- Create: `tests/test_api_prefix.py`

**Interfaces:**
- Produces: Flask URL rules `GET /api/health` and `GET /api/characters`; no rule at `/health` or `/characters`. Tasks 2 and 3 rely on these paths.

- [ ] **Step 1: Write the failing test** in `tests/test_api_prefix.py`. A fixture sets `DATABASE_USERNAME`, `DATABASE_HOST`, `DATABASE_NAME` via `monkeypatch` and returns `create_app()` (engine creation is lazy, so no DB is needed). Tests:
  - `test_prefixed_routes_registered`: `{r.rule for r in app.url_map.iter_rules()}` contains `/api/health` and `/api/characters`.
  - `test_unprefixed_routes_absent`: that set contains neither `/health` nor `/characters`.
  - `test_unprefixed_path_is_404`: `app.test_client().get("/characters").status_code == 404` and the same for `/health`.

- [ ] **Step 2: Run** `uv run pytest tests/test_api_prefix.py -v`. Expected: the three tests FAIL (prefixed rules missing / unprefixed present).

- [ ] **Step 3: Implement.** Change `characters_bp` to `url_prefix="/api/characters"`, and change the health route decorator in `create_app` to `@app.get("/api/health")`.

- [ ] **Step 4: Run** `uv run pytest tests/test_api_prefix.py -v`. Expected: 3 PASS.

---

### Task 2: nginx config and placeholder frontend

**Files:**
- Create: `src/sbapi/infra/local/nginx/nginx.conf`
- Create: `src/sbapi/infra/local/web/index.html`

**Interfaces:**
- Consumes: the app is reachable as service name `app` on port 8080 and serves `/api/*` (Task 1).
- Produces: a config file intended to be mounted at `/etc/nginx/conf.d/default.conf`, and a web root intended for `/usr/share/nginx/html`. Task 3 mounts both. The file is a `conf.d` fragment, so it contains `server`-level config plus `http`-level directives (`log_format`, `limit_req_zone`) only, no `events`/`http` wrapper.

- [ ] **Step 1: Write `nginx.conf`** with:
  - `log_format` named `upstream_log` that includes `$remote_addr`, `$request`, `$status`, `$upstream_addr`, `$request_time`; `access_log /dev/stdout upstream_log;`.
  - `limit_req_zone $binary_remote_addr zone=api:10m rate=20r/s;`.
  - `resolver 127.0.0.11 valid=5s ipv6=off;` and, in `location /api/`, `set $api_upstream http://app:8080;` then `proxy_pass $api_upstream;` (variable form so Docker DNS is re-resolved every 5s; with a variable and no URI part, nginx forwards the original `/api/...` URI unchanged).
  - In `location /api/`: `proxy_set_header Host $host; X-Forwarded-For $proxy_add_x_forwarded_for; X-Forwarded-Proto $scheme;` `limit_req zone=api burst=40 nodelay; limit_req_status 429;` `proxy_connect_timeout 2s; proxy_read_timeout 30s;` and `proxy_next_upstream error timeout http_502 http_503;`.
  - `gzip on;` with `gzip_types application/json text/css application/javascript;`.
  - `location /` with `root /usr/share/nginx/html; try_files $uri /index.html;`.

- [ ] **Step 2: Write `index.html`**, a minimal page titled "SBAPI" stating the frontend isn't built yet and linking to `/api/health`.

- [ ] **Step 3: Validate syntax** with `docker run --rm -v "$PWD/src/sbapi/infra/local/nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro" nginx:alpine nginx -t`. Expected: `syntax is ok` (the unresolvable `app` host is fine because the upstream is a variable).

---

### Task 3: Compose wiring, docs and end-to-end verification

**Files:**
- Modify: `sbapi-compose.yaml`
- Modify: `.envexample` (add `PROXY_HOST_PORT=8080`, `APP_REPLICAS=3`)
- Modify: `README.md` (stack/layout, local development, curl examples now `localhost:8080/api/...`, note populate still uses the loopback DB port)

**Interfaces:**
- Consumes: nginx config and web root from Task 2; `/api/health` from Task 1.

- [ ] **Step 1: Edit `sbapi-compose.yaml`:**
  - `db`: ports become `"127.0.0.1:${DB_HOST_PORT:-5432}:5432"`.
  - `app`: remove `ports`; add `deploy: {replicas: ${APP_REPLICAS:-3}}`; add env `FORWARDED_ALLOW_IPS: "*"`; healthcheck URL becomes `http://localhost:8080/api/health`.
  - New `proxy` service: `image: nginx:alpine`, `restart: unless-stopped`, `ports: ["${PROXY_HOST_PORT:-8080}:80"]`, volumes mounting `./src/sbapi/infra/local/nginx/nginx.conf` to `/etc/nginx/conf.d/default.conf:ro` and `./src/sbapi/infra/local/web` to `/usr/share/nginx/html:ro`, `depends_on: app: condition: service_healthy`.

- [ ] **Step 2: Bring it up.** Run `docker compose -f sbapi-compose.yaml up --build -d` then `docker compose -f sbapi-compose.yaml ps`. Expected: `db`, `proxy` and three `app` containers running, apps `healthy`.

- [ ] **Step 3: Verify routing and balancing.**
  - `curl -s localhost:8080/api/health` returns `{"status":"ok"}`; `curl -s localhost:8080/api/characters` returns a JSON array.
  - `curl -s localhost:8080/` returns the placeholder HTML.
  - Run `for i in 1 2 3 4 5 6; do curl -s -o /dev/null localhost:8080/api/health; done` then `docker compose -f sbapi-compose.yaml logs proxy`. Expected: at least 3 distinct `upstream_addr` values.
  - Review Focus 1: `curl -s -o /dev/null -w '%{http_code}\n' localhost:8080/health` is not 200 API data (placeholder page or 404 is fine; it must not return `{"status":"ok"}`), and likewise for `/characters`.
  - Review Focus 3: `curl -si localhost:8080/api/nope` returns 404 with a non-placeholder body (no "frontend isn't built" text).

- [ ] **Step 4: Verify resilience.**
  - Review Focus 2: `docker compose -f sbapi-compose.yaml restart app`, wait for healthy, then 10 requests to `/api/health` all return 200 (also run once with one replica stopped via `docker stop <one app container>`; requests still succeed).
  - Review Focus 4: `docker compose -f sbapi-compose.yaml stop db`; `curl -s -o /dev/null -w '%{http_code} %{time_total}\n' localhost:8080/api/health` returns a 5xx in under 5s. Then `start db` again and confirm 200.

- [ ] **Step 5: Verify populate and docs.**
  - Review Focus 5: with the stack up and `.env` pointing at `localhost:5432`, `uv run populate` completes without connection errors.
  - Run `uv run pytest -v`. Expected: all pass. Skim the README diff to confirm no stale `localhost:8000` or unprefixed curl examples remain (`grep -n "8000\|/health\|/characters" README.md`).

- [ ] **Step 6: Tear down** with `docker compose -f sbapi-compose.yaml down` (keep the volume).
