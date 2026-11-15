# Local infra: nginx in front of replicated Gunicorn

Status: awaiting approval

## Intent

Get a realistic local stack before designing AWS: one entry point, several
identical API replicas behind it, and a slot for a frontend that doesn't exist
yet. The same app image and the same URL layout should carry over to AWS, where
an ALB (plus CloudFront/S3 for the frontend) replaces nginx. Nothing the app
needs to work should live only in the nginx config.

## Goals

- One published port. nginx routes `/api/*` to the API and `/` to a static
  frontend slot (placeholder page for now).
- The API runs as N replicas (default 3) behind nginx, so load balancing and
  replica failure are visible locally.
- API served under an `/api` prefix, implemented in the Flask app (not an nginx
  rewrite), so it behaves identically behind nginx or an ALB path rule.
- Fix the existing port mismatch (Dockerfile binds 8080, compose publishes and
  health-checks 8000).

## Non-goals

HAProxy, TLS, Redis/caching, metrics/dashboards, CORS (frontend will be
same-origin through nginx; add it in the app when a cross-origin consumer
exists), the frontend itself, CI changes, and any Terraform/AWS work.

## Approaches considered

- **A. Plain nginx + replicas**, API at the root. Quickest, but the frontend
  and API would collide at `/` and diverge from ALB path routing.
- **B. Mirror the AWS shape** (chosen): `/api` prefix in the app, nginx as the
  single entry point, frontend slot at `/`.
- **C. B plus Redis and Prometheus/Grafana.** Deferred; nothing needs them yet.

## Design

**Services (`sbapi-compose.yaml`)**
- `proxy`: `nginx:alpine`, the only service published to the host
  (`${PROXY_HOST_PORT:-8080}:80`). Mounts the nginx config and the web folder
  read-only.
- `app`: built from the existing Dockerfile, `deploy.replicas: 3`, no host
  port, listening on 8080 in the container. Healthcheck targets
  `/api/health` on 8080.
- `db`: unchanged, except its host port binds to `127.0.0.1` only so the
  populate scripts keep working from the host.

**nginx**
- `/api/` proxies to the `app` service name (Docker DNS, round robin) with
  `Host`, `X-Forwarded-For` and `X-Forwarded-Proto` set.
- `/` serves a static root with a placeholder `index.html`.
- gzip for JSON, and a generous per-IP `limit_req` on `/api/` as a local
  stand-in for what WAF would do on AWS.
- Access log includes `$upstream_addr` so you can see requests spread across
  replicas.

**App**
- `characters_bp` prefix becomes `/api/characters`; `/health` becomes
  `/api/health`. No other behaviour change.
- Gunicorn trusts the proxy's forwarded headers (`FORWARDED_ALLOW_IPS` set in
  compose, safe because the network is private to the compose project).
- Gunicorn settings otherwise unchanged (sync workers, `SBAPI_WORKERS`).

**Files**
- `src/sbapi/infra/local/nginx/nginx.conf`
- `src/sbapi/infra/local/web/index.html` (placeholder)
- edits: `sbapi-compose.yaml`, `Dockerfile` (comment/consistency only),
  `src/sbapi/app/main.py`, `src/sbapi/app/routes/sbapi_flask_route_characters.py`,
  `README.md`, `.envexample`

## Verification

- `docker compose -f sbapi-compose.yaml up --build` comes up healthy.
- `curl localhost:8080/api/health` and `/api/characters` succeed; repeated
  calls show different `upstream_addr` values in the proxy log.
- `curl localhost:8080/` returns the placeholder page.
- Stopping one `app` replica doesn't fail requests (nginx retries/skips it).
- Old unprefixed paths (`/health`, `/characters`) return 404 or the placeholder,
  not API data.

## Left to the builder

- Making nginx tolerate replica restarts (re-resolving `app` through Docker's
  resolver vs. a fixed upstream list).
- Exact rate-limit numbers, timeouts and gzip types.

## Calls I made (not discussed)

- **nginx, not HAProxy.** nginx also serves the static frontend; HAProxy can't.
  Both are interchangeable for the proxying part.
- `db` keeps a loopback-only host port instead of being unpublished, so
  `uv run populate` still works.
- Local infra lives in `src/sbapi/infra/local/`, next to the Terraform.
- Health moves to `/api/health` so the ALB target-group check and the compose
  check use the same path.
- CORS is out of scope until there's a cross-origin consumer.
