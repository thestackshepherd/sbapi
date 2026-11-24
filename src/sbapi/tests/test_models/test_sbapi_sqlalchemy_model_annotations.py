"""Tests for the Trivia and Citation models."""

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from sbapi.app.models import Citation, Trivia

# FK column -> fixture that provides a row of that entity
TRIVIA_TARGETS = [
    ("character_id", "character"),
    ("planet_id", "planet"),
    ("vehicle_id", "vehicle"),
    ("item_id", "item"),
    ("actor_id", "actor"),
]
CITATION_TARGETS = [*TRIVIA_TARGETS, ("quote_id", "quote")]


def _trivia(**target) -> Trivia:
    return Trivia(trivia_text="a note", **target)


def _citation(**target) -> Citation:
    return Citation(citation_number=1, source_text="Spaceballs (1987 film)", **target)


class TestTrivia:
    def test_table_definition(self):
        table = Trivia.__table__
        assert table.name == "trivia"
        assert table.c.trivia_kind.nullable is False
        index_names = {index.name for index in table.indexes}
        assert {f"idx_trivia_{fk}" for fk, _ in TRIVIA_TARGETS} == index_names

    @pytest.mark.parametrize(("fk", "fixture"), TRIVIA_TARGETS)
    def test_attaches_to_each_entity_type(self, session, request, fk, fixture):
        entity = request.getfixturevalue(fixture)
        session.add(_trivia(**{fk: entity.id}))
        session.commit()
        assert getattr(session.scalar(select(Trivia)), fk) == entity.id

    def test_kind_defaults_to_trivia(self, session, character):
        row = _trivia(character_id=character.id)
        session.add(row)
        session.commit()
        session.refresh(row)
        assert row.trivia_kind == "trivia"

    @pytest.mark.parametrize("kind", ["trivia", "behind_the_scenes"])
    def test_accepts_valid_kinds(self, session, character, kind):
        session.add(_trivia(character_id=character.id, trivia_kind=kind))
        session.commit()
        assert session.scalar(select(Trivia)).trivia_kind == kind

    def test_rejects_unknown_kind(self, session, character):
        session.add(_trivia(character_id=character.id, trivia_kind="gossip"))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_must_name_an_entity(self, session):
        session.add(_trivia())
        with pytest.raises(IntegrityError):
            session.commit()

    def test_cannot_name_two_entities(self, session, character, planet):
        session.add(_trivia(character_id=character.id, planet_id=planet.id))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_entity_must_exist(self, session):
        session.add(_trivia(character_id=9999))
        with pytest.raises(IntegrityError):
            session.commit()

    @pytest.mark.parametrize(("fk", "fixture"), TRIVIA_TARGETS)
    def test_deleting_the_entity_deletes_its_trivia(
        self, session, request, fk, fixture
    ):
        entity = request.getfixturevalue(fixture)
        session.add(_trivia(**{fk: entity.id}))
        session.commit()

        session.delete(entity)
        session.commit()

        assert session.scalars(select(Trivia)).all() == []


class TestCitation:
    def test_table_definition(self):
        table = Citation.__table__
        assert table.name == "citations"
        assert table.c.citation_number.nullable is False
        assert table.c.source_text.nullable is False
        assert table.c.source_url.nullable is True
        index_names = {index.name for index in table.indexes}
        assert {f"idx_citations_{fk}" for fk, _ in CITATION_TARGETS} == index_names

    @pytest.mark.parametrize(("fk", "fixture"), CITATION_TARGETS)
    def test_attaches_to_each_entity_type(self, session, request, fk, fixture):
        entity = request.getfixturevalue(fixture)
        session.add(_citation(**{fk: entity.id}))
        session.commit()
        assert getattr(session.scalar(select(Citation)), fk) == entity.id

    def test_persists_source_url(self, session, character):
        session.add(
            _citation(
                character_id=character.id,
                source_url="https://spaceballs.fandom.com/wiki/Lone_Starr",
            )
        )
        session.commit()
        assert session.scalar(select(Citation)).source_url.endswith("Lone_Starr")

    def test_source_text_is_required(self, session, character):
        session.add(Citation(citation_number=1, character_id=character.id))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_citation_number_is_required(self, session, character):
        session.add(Citation(source_text="Spaceballs", character_id=character.id))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_must_name_an_entity(self, session):
        session.add(_citation())
        with pytest.raises(IntegrityError):
            session.commit()

    def test_cannot_name_two_entities(self, session, character, quote):
        session.add(_citation(character_id=character.id, quote_id=quote.id))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_entity_must_exist(self, session):
        session.add(_citation(quote_id=9999))
        with pytest.raises(IntegrityError):
            session.commit()

    @pytest.mark.parametrize(("fk", "fixture"), CITATION_TARGETS)
    def test_deleting_the_entity_deletes_its_citations(
        self, session, request, fk, fixture
    ):
        entity = request.getfixturevalue(fixture)
        session.add(_citation(**{fk: entity.id}))
        session.commit()

        session.delete(entity)
        session.commit()

        assert session.scalars(select(Citation)).all() == []
