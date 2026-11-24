"""
Shared pytest fixtures for the model and repository tests.

Tests run against an in-memory SQLite database built from the ORM models, so no
Postgres is needed. Two Postgres behaviours are emulated on every connection:
foreign keys are enforced (ON DELETE CASCADE / SET NULL), and the
num_nonnulls() function used by the trivia and citations CHECK constraints.
"""

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from sbapi.app.models import Actor, Base, Character, Item, Planet, Quote, Vehicle


def _emulate_postgres(dbapi_connection, _connection_record) -> None:
    dbapi_connection.create_function(
        "num_nonnulls",
        -1,
        lambda *args: sum(arg is not None for arg in args),
        deterministic=True,
    )
    dbapi_connection.execute("PRAGMA foreign_keys=ON")


@pytest.fixture
def engine():
    engine = create_engine("sqlite://")
    event.listen(engine, "connect", _emulate_postgres)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session


def _persist(session: Session, row):
    session.add(row)
    session.commit()
    return row


@pytest.fixture
def planet(session):
    return _persist(session, Planet(name="Druidia"))


@pytest.fixture
def actor(session):
    return _persist(session, Actor(actor_name="Bill Pullman"))


@pytest.fixture
def character(session):
    return _persist(session, Character(character_name="Lone Starr"))


@pytest.fixture
def vehicle(session):
    return _persist(session, Vehicle(vehicle_name="Eagle 5"))


@pytest.fixture
def item(session):
    return _persist(session, Item(item_name="The Schwartz", item_type="other"))


@pytest.fixture
def quote(session):
    return _persist(session, Quote(quote_text="A hundred thousand spacebucks!?"))
