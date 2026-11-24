"""Tests for the Item model."""

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from sbapi.app.models import Character, Citation, Item, Trivia

ITEM_TYPES = ["weapon", "artifact", "tech", "merchandise", "other"]


class TestItem:
    def test_table_definition(self):
        table = Item.__table__
        assert table.name == "items"
        assert table.c.item_name.nullable is False
        assert table.c.item_type.nullable is False
        for column in (
            "description",
            "parody_of",
            "owner_character_id",
            "image_url",
            "source_url",
            "last_updated",
        ):
            assert table.c[column].nullable is True, column
        index_names = {index.name for index in table.indexes}
        assert {"idx_items_name", "idx_items_owner_character_id"} <= index_names

    @pytest.mark.parametrize("item_type", ITEM_TYPES)
    def test_accepts_every_item_type(self, session, item_type):
        session.add(Item(item_name=f"a {item_type}", item_type=item_type))
        session.commit()
        assert session.scalar(select(Item)).item_type == item_type

    def test_rejects_unknown_item_type(self, session):
        session.add(Item(item_name="Spaceballs: The Flamethrower", item_type="toy"))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_item_name_is_required(self, session):
        session.add(Item(item_type="other"))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_item_type_is_required(self, session):
        session.add(Item(item_name="The Schwartz"))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_persists_optional_columns(self, session):
        session.add(
            Item(
                item_name="The Schwartz",
                item_type="other",
                description="Supernatural force.",
                parody_of="The Force (Star Wars)",
                source_url="https://spaceballs.fandom.com/wiki/The_Schwartz",
            )
        )
        session.commit()

        item = session.scalar(select(Item))
        assert item.description == "Supernatural force."
        assert item.parody_of == "The Force (Star Wars)"
        assert item.owner_character_id is None


class TestItemOwner:
    def test_owner_and_items_are_linked(self, session, character):
        ring = Item(
            item_name="Ring of the Schwartz", item_type="weapon", owner=character
        )
        session.add(ring)
        session.commit()

        assert ring.owner_character_id == character.id
        assert character.items == [ring]

    def test_owner_must_exist(self, session):
        session.add(Item(item_name="Ring", item_type="weapon", owner_character_id=9999))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_deleting_owner_keeps_the_item(self, session, character):
        ring = Item(
            item_name="Ring of the Schwartz", item_type="weapon", owner=character
        )
        session.add(ring)
        session.commit()

        session.delete(character)
        session.commit()

        assert session.get(Item, ring.id).owner_character_id is None
        assert session.get(Character, character.id) is None


class TestItemRelationships:
    def test_collections_start_empty(self, item):
        assert item.owner is None
        assert item.trivia == []
        assert item.citations == []

    def test_trivia_and_citations_attach_by_item_id(self, session, item):
        session.add_all(
            [
                Trivia(trivia_text="a note", item_id=item.id),
                Citation(citation_number=1, source_text="Spaceballs", item_id=item.id),
            ]
        )
        session.commit()
        assert len(item.trivia) == 1
        assert len(item.citations) == 1

    def test_delete_cascades_annotations(self, session, item):
        session.add_all(
            [
                Trivia(trivia_text="a note", item_id=item.id),
                Citation(citation_number=1, source_text="Spaceballs", item_id=item.id),
            ]
        )
        session.commit()

        session.delete(item)
        session.commit()

        assert session.scalars(select(Trivia)).all() == []
        assert session.scalars(select(Citation)).all() == []
