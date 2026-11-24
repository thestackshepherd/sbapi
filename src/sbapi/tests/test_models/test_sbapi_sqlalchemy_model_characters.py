"""Tests for the Character model."""

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from sbapi.app.models import (
    Character,
    CharacterActor,
    Citation,
    Item,
    Quote,
    Trivia,
    VehicleCrew,
)


class TestCharacterTable:
    def test_table_definition(self):
        table = Character.__table__
        assert table.name == "characters"
        assert table.c.character_name.nullable is False
        for column in (
            "full_name",
            "species",
            "gender",
            "character_role",
            "parody_of",
            "homeworld_id",
            "image_url",
            "source_url",
            "last_updated",
        ):
            assert table.c[column].nullable is True, column
        index_names = {index.name for index in table.indexes}
        assert {"idx_characters_name", "idx_characters_homeworld_id"} <= index_names

    def test_persists_all_columns(self, session, planet):
        session.add(
            Character(
                character_name="Dark Helmet",
                full_name="Dark Helmet",
                species="Human",
                gender="Male",
                character_role="Commander of Spaceball One",
                parody_of="Darth Vader",
                homeworld_id=planet.id,
                source_url="https://spaceballs.fandom.com/wiki/Dark_Helmet",
            )
        )
        session.commit()

        helmet = session.scalar(select(Character))
        assert helmet.character_name == "Dark Helmet"
        assert helmet.parody_of == "Darth Vader"
        assert helmet.homeworld_id == planet.id

    def test_character_name_is_required(self, session):
        session.add(Character())
        with pytest.raises(IntegrityError):
            session.commit()

    def test_duplicate_names_are_allowed(self, session, character):
        session.add(Character(character_name=character.character_name))
        session.commit()
        assert len(session.scalars(select(Character)).all()) == 2


class TestCharacterHomeworld:
    def test_homeworld_and_natives_are_linked(self, session, planet):
        barf = Character(character_name="Barf", homeworld=planet)
        session.add(barf)
        session.commit()

        assert barf.homeworld_id == planet.id
        assert planet.natives == [barf]

    def test_homeworld_must_exist(self, session):
        session.add(Character(character_name="Barf", homeworld_id=9999))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_deleting_planet_clears_homeworld(self, session, planet):
        barf = Character(character_name="Barf", homeworld=planet)
        session.add(barf)
        session.commit()

        session.delete(planet)
        session.commit()

        assert session.get(Character, barf.id).homeworld_id is None


class TestCharacterRelationships:
    def test_collections_start_empty(self, character):
        assert character.actor_links == []
        assert character.crew_roles == []
        assert character.quotes == []
        assert character.items == []
        assert character.trivia == []
        assert character.citations == []

    def test_collections_load_related_rows(self, session, actor, vehicle, character):
        session.add_all(
            [
                CharacterActor(character_id=character.id, actor_id=actor.id),
                VehicleCrew(vehicle_id=vehicle.id, character_id=character.id),
                Quote(
                    quote_text="A hundred thousand spacebucks!?", character=character
                ),
                Item(item_name="Ring", item_type="weapon", owner=character),
                Trivia(trivia_text="a note", character_id=character.id),
                Citation(
                    citation_number=1,
                    source_text="Spaceballs",
                    character_id=character.id,
                ),
            ]
        )
        session.commit()

        assert len(character.actor_links) == 1
        assert len(character.crew_roles) == 1
        assert len(character.quotes) == 1
        assert len(character.items) == 1
        assert len(character.trivia) == 1
        assert len(character.citations) == 1

    def test_delete_cascades_to_owned_rows_and_nulls_the_rest(
        self, session, actor, vehicle, character
    ):
        """Regression: deleting a character must let the database cascade."""
        character_id, actor_id, vehicle_id = character.id, actor.id, vehicle.id
        quote = Quote(quote_text="A hundred thousand spacebucks!?", character=character)
        item = Item(item_name="Ring", item_type="weapon", owner=character)
        session.add_all(
            [
                CharacterActor(character_id=character_id, actor_id=actor_id),
                VehicleCrew(vehicle_id=vehicle_id, character_id=character_id),
                quote,
                item,
                Trivia(trivia_text="a note", character_id=character_id),
                Citation(
                    citation_number=1,
                    source_text="Spaceballs",
                    character_id=character_id,
                ),
            ]
        )
        session.commit()

        session.delete(character)
        session.commit()

        # cascaded away
        assert session.scalars(select(CharacterActor)).all() == []
        assert session.scalars(select(VehicleCrew)).all() == []
        assert session.scalars(select(Trivia)).all() == []
        assert session.scalars(select(Citation)).all() == []
        # kept, but no longer attached to a character
        assert session.get(Quote, quote.id).character_id is None
        assert session.get(Item, item.id).owner_character_id is None
