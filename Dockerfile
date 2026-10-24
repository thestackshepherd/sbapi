FROM python:3.14-slim

RUN mkdir -p /app

WORKDIR /app

# Workspace manifests first so the dependency layer caches. Every member's
# pyproject.toml must be present, even though only sbapi_api is installed.
COPY .python-version pyproject.toml uv.lock ./
COPY sbapi_api/pyproject.toml sbapi_api/pyproject.toml
COPY sbapi_scripts/pyproject.toml sbapi_scripts/pyproject.toml
RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev --package sbapi_api --no-install-workspace

COPY sbapi_api ./sbapi_api
RUN uv sync --frozen --no-dev --package sbapi_api

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "--package", "sbapi_api", "gunicorn", "--bind", "0.0.0.0:8000", "sbapi_api.wsgi:app"]
