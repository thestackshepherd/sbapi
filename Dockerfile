FROM python:3.14-slim

RUN mkdir -p /app

WORKDIR /app

COPY .python-version pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev

COPY src ./src

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "sbapi.wsgi:app"]