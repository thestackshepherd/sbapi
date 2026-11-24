"""Tests for the Planet model."""

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from sbapi.app.models import Character, Citation, Planet, Trivia


class TestPlanet:
    def test_table_definition(self):
        table = Planet.__table__
        assert table.name == "planets"
        assert table.c.name.nullable is False
        for column in (
            "ruler_id",
            "planet_type",
            "description",
            "government",
            "capital",
            "parody_of",
            "last_updated",
        ):
            assert table.c[column].nullable is True, column
        assert "idx_planets" in {index.name for index in table.indexes}

    def test_persists_all_columns(self, session):
        session.add(
            Planet(
                name="Planet Spaceball",
                ruler_id="skroob",
                planet_type="planet",
                description="Home of the Spaceballs.",
                government="presidency",
                capital="Spaceball City",
                parody_of="Galactic Empire (Star Wars)",
            )
        )
        session.commit()

        planet = session.scalar(select(Planet))
        assert planet.name == "Planet Spaceball"
        assert planet.government == "presidency"
        assert planet.capital == "Spaceball City"

    def test_name_is_required(self, session):
        session.add(Planet())
        with pytest.raises(IntegrityError):
            session.commit()

    def test_optional_columns_default_to_none(self, planet):
        assert planet.ruler_id is None
        assert planet.description is None
        assert planet.last_updated is None


class TestPlanetRelationships:
    def test_collections_start_empty(self, planet):
        assert planet.natives == []
        assert planet.trivia == []
        assert planet.citations == []

    def test_natives_lists_characters_with_this_homeworld(self, session, planet):
        session.add_all(
            [
                Character(character_name="Vespa", homeworld=planet),
                Character(character_name="Roland", homeworld=planet),
            ]
        )
        session.commit()
        assert {c.character_name for c in planet.natives} == {"Vespa", "Roland"}

    def test_trivia_and_citations_attach_by_planet_id(self, session, planet):
        session.add_all(
            [
                Trivia(trivia_text="a note", planet_id=planet.id),
                Citation(
                    citation_number=1, source_text="Spaceballs", planet_id=planet.id
                ),
            ]
        )
        session.commit()
        assert len(planet.trivia) == 1
        assert len(planet.citations) == 1

    def test_delete_cascades_annotations_and_keeps_natives(self, session, planet):
        """Regression: deleting a planet must let the database cascade."""
        planet_id = planet.id
        vespa = Character(character_name="Vespa", homeworld=planet)
        session.add_all(
            [
                vespa,
                Trivia(trivia_text="a note", planet_id=planet_id),
                Citation(
                    citation_number=1, source_text="Spaceballs", planet_id=planet_id
                ),
            ]
        )
        session.commit()

        session.delete(planet)
        session.commit()

        assert session.scalars(select(Trivia)).all() == []
        assert session.scalars(select(Citation)).all() == []
        assert session.get(Character, vespa.id).homeworld_id is None
