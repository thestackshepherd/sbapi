"""Tests for the Quote model."""

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from sbapi.app.models import Character, Citation, Quote


class TestQuote:
    def test_table_definition(self):
        table = Quote.__table__
        assert table.name == "quotes"
        assert table.c.quote_text.nullable is False
        assert table.c.character_id.nullable is True
        assert table.c.source_url.nullable is True
        assert table.c.last_updated.nullable is True
        assert "idx_quotes_character_id" in {index.name for index in table.indexes}

    def test_persists_and_reads_back(self, session):
        session.add(
            Quote(
                quote_text="A hundred thousand spacebucks!?",
                source_url="https://spaceballs.fandom.com/wiki/Spacebucks",
            )
        )
        session.commit()

        quote = session.scalar(select(Quote))
        assert quote.quote_text == "A hundred thousand spacebucks!?"
        assert quote.character_id is None

    def test_quote_text_is_required(self, session):
        session.add(Quote())
        with pytest.raises(IntegrityError):
            session.commit()

    def test_character_is_optional(self, quote):
        assert quote.character is None
        assert quote.citations == []


class TestQuoteCharacter:
    def test_character_and_quotes_are_linked(self, session, character):
        quote = Quote(quote_text="A hundred thousand spacebucks!?", character=character)
        session.add(quote)
        session.commit()

        assert quote.character_id == character.id
        assert character.quotes == [quote]

    def test_character_must_exist(self, session):
        session.add(
            Quote(quote_text="A hundred thousand spacebucks!?", character_id=9999)
        )
        with pytest.raises(IntegrityError):
            session.commit()

    def test_deleting_character_keeps_the_quote(self, session, character):
        quote = Quote(quote_text="A hundred thousand spacebucks!?", character=character)
        session.add(quote)
        session.commit()

        session.delete(character)
        session.commit()

        assert session.get(Character, character.id) is None
        assert session.get(Quote, quote.id).character_id is None


class TestQuoteCitations:
    def test_citations_attach_by_quote_id(self, session, quote):
        session.add(
            Citation(citation_number=1, source_text="Spaceballs", quote_id=quote.id)
        )
        session.commit()
        assert len(quote.citations) == 1

    def test_delete_cascades_citations(self, session, quote):
        session.add(
            Citation(citation_number=1, source_text="Spaceballs", quote_id=quote.id)
        )
        session.commit()

        session.delete(quote)
        session.commit()

        assert session.scalars(select(Citation)).all() == []
