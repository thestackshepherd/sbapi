import pytest

from sbapi.app.main import create_app


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv("DATABASE_USERNAME", "test")
    monkeypatch.setenv("DATABASE_HOST", "localhost")
    monkeypatch.setenv("DATABASE_NAME", "test")
    return create_app()


def _rules(app):
    return {r.rule for r in app.url_map.iter_rules()}


def test_prefixed_routes_registered(app):
    rules = _rules(app)
    assert "/api/health" in rules
    assert "/api/characters" in rules


def test_unprefixed_routes_absent(app):
    rules = _rules(app)
    assert "/health" not in rules
    assert "/characters" not in rules


def test_unprefixed_path_is_404(app):
    client = app.test_client()
    assert client.get("/characters").status_code == 404
    assert client.get("/health").status_code == 404
