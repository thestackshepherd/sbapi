"""Annotation tables shared by every entity.

Each row points at exactly one entity: one nullable FK per entity type, with a
CHECK that exactly one is set.
"""
from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from sbapi_api.models.sbapi_sqlalchemy_model_base import Base


class Trivia(Base):
    """trivia database table model (trivia and behind-the-scenes notes)"""

    __tablename__ = "trivia"
    __table_args__ = (
        CheckConstraint("trivia_kind IN ('trivia', 'behind_the_scenes')"),
        CheckConstraint(
            "num_nonnulls(character_id, location_id, faction_id, vehicle_id, "
            "item_id, media_id, episode_id, actor_id) = 1"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trivia_kind: Mapped[str] = mapped_column(String, server_default="trivia")
    trivia_text: Mapped[str] = mapped_column(Text)
    character_id: Mapped[Optional[int]] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"), index=True)
    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"), index=True)
    faction_id: Mapped[Optional[int]] = mapped_column(ForeignKey("factions.id", ondelete="CASCADE"), index=True)
    vehicle_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vehicles.id", ondelete="CASCADE"), index=True)
    item_id: Mapped[Optional[int]] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"), index=True)
    media_id: Mapped[Optional[int]] = mapped_column(ForeignKey("media.id", ondelete="CASCADE"), index=True)
    episode_id: Mapped[Optional[int]] = mapped_column(ForeignKey("episodes.id", ondelete="CASCADE"), index=True)
    actor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("actors.id", ondelete="CASCADE"), index=True)


class Citation(Base):
    """citations database table model (numbered sources backing an entity's data)"""

    __tablename__ = "citations"
    __table_args__ = (
        CheckConstraint(
            "num_nonnulls(character_id, location_id, faction_id, vehicle_id, "
            "item_id, media_id, episode_id, actor_id, quote_id) = 1"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    citation_number: Mapped[int] = mapped_column(Integer)
    source_text: Mapped[str] = mapped_column(Text)
    source_url: Mapped[Optional[str]] = mapped_column(String)
    character_id: Mapped[Optional[int]] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"), index=True)
    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"), index=True)
    faction_id: Mapped[Optional[int]] = mapped_column(ForeignKey("factions.id", ondelete="CASCADE"), index=True)
    vehicle_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vehicles.id", ondelete="CASCADE"), index=True)
    item_id: Mapped[Optional[int]] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"), index=True)
    media_id: Mapped[Optional[int]] = mapped_column(ForeignKey("media.id", ondelete="CASCADE"), index=True)
    episode_id: Mapped[Optional[int]] = mapped_column(ForeignKey("episodes.id", ondelete="CASCADE"), index=True)
    actor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("actors.id", ondelete="CASCADE"), index=True)
    quote_id: Mapped[Optional[int]] = mapped_column(ForeignKey("quotes.id", ondelete="CASCADE"), index=True)
