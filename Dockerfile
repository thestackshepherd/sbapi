FROM python:3.15-slim

# uv comes from its official image, pinned by version and digest, instead of an
# unpinned `pip install uv` that could pull (and build) anything at build time.
COPY --from=ghcr.io/astral-sh/uv:0.13.8@sha256:5cc1805e2426484abca4ad46ea783bab281fdb225fd82d8ce6d66a81254bac85 /uv /usr/local/bin/uv

ENV UV_NO_CACHE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# --frozen: install exactly what uv.lock pins. --no-build: wheels only, so no
# third-party setup script runs during the build (the local project is exempt).
COPY .python-version pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-build --no-install-project

COPY README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev --no-build

# Run as an unprivileged user. It only needs to read /app; gunicorn keeps its
# control socket under $HOME.
RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin sbapi
USER sbapi

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "sbapi.app.wsgi:app"]
