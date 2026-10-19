FROM python:3.14-slim

RUN mkdir -p /app

WORKDIR /app

COPY .python-version pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev --no-install-project

COPY README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "gunicorn", "--bind", "0.0.0.0:8000", "sbapi.app.wsgi:app"]
