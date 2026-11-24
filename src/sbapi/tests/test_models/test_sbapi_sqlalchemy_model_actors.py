"""Tests for the Actor and CharacterActor models."""

from datetime import UTC, datetime

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from sbapi.app.models import Actor, Character, CharacterActor


class TestActor:
    def test_table_definition(self):
        table = Actor.__table__
        assert table.name == "actors"
        assert table.c.actor_name.nullable is False
        assert table.c.last_updated.nullable is True
        assert "idx_actors" in {index.name for index in table.indexes}

    def test_persists_and_reads_back(self, session):
        stamp = datetime.now(UTC)
        session.add(Actor(actor_name="Rick Moranis", last_updated=stamp))
        session.commit()

        actor = session.scalar(select(Actor).where(Actor.actor_name == "Rick Moranis"))
        assert actor.id is not None
        assert actor.last_updated is not None

    def test_last_updated_is_optional(self, actor):
        assert actor.last_updated is None

    def test_actor_name_is_required(self, session):
        session.add(Actor())
        with pytest.raises(IntegrityError):
            session.commit()

    def test_actor_name_is_unique(self, session, actor):
        session.add(Actor(actor_name=actor.actor_name))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_character_links_starts_empty(self, actor):
        assert actor.character_links == []

    def test_delete_cascades_to_character_links(self, session, actor, character):
        session.add(CharacterActor(character_id=character.id, actor_id=actor.id))
        session.commit()

        session.delete(actor)
        session.commit()

        assert session.scalars(select(CharacterActor)).all() == []


class TestCharacterActor:
    def test_table_definition(self):
        table = CharacterActor.__table__
        assert table.name == "character_actors"
        assert table.c.character_id.nullable is False
        assert table.c.actor_id.nullable is False
        assert table.c.credit_type.nullable is True
        assert table.c.notes.nullable is True
        assert "idx_character_actors_actor_id" in {i.name for i in table.indexes}

    @pytest.mark.parametrize("credit_type", ["live_action", "voice", None])
    def test_accepts_valid_credit_types(self, session, actor, character, credit_type):
        link = CharacterActor(
            character_id=character.id, actor_id=actor.id, credit_type=credit_type
        )
        session.add(link)
        session.commit()
        assert link.credit_type == credit_type

    def test_rejects_unknown_credit_type(self, session, actor, character):
        session.add(
            CharacterActor(
                character_id=character.id, actor_id=actor.id, credit_type="cameo"
            )
        )
        with pytest.raises(IntegrityError):
            session.commit()

    def test_character_and_actor_pair_is_unique(self, session, actor, character):
        session.add(CharacterActor(character_id=character.id, actor_id=actor.id))
        session.commit()
        session.add(CharacterActor(character_id=character.id, actor_id=actor.id))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_same_actor_can_play_several_characters(self, session, actor, character):
        other = Character(character_name="Barf")
        session.add(other)
        session.commit()
        session.add_all(
            [
                CharacterActor(character_id=character.id, actor_id=actor.id),
                CharacterActor(character_id=other.id, actor_id=actor.id),
            ]
        )
        session.commit()
        assert len(actor.character_links) == 2

    def test_requires_existing_character_and_actor(self, session, actor):
        session.add(CharacterActor(character_id=9999, actor_id=actor.id))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_relationships_resolve_both_sides(self, session, actor, character):
        link = CharacterActor(character=character, actor=actor, notes="lead role")
        session.add(link)
        session.commit()

        assert link.character is character
        assert link.actor is actor
        assert character.actor_links == [link]
        assert actor.character_links == [link]

    def test_deleting_character_removes_link(self, session, actor, character):
        session.add(CharacterActor(character_id=character.id, actor_id=actor.id))
        session.commit()

        session.delete(character)
        session.commit()

        assert session.scalars(select(CharacterActor)).all() == []
        assert session.get(Actor, actor.id) is not None
