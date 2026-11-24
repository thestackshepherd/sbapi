"""
SQLAlchemy ORM Model file represents the Actors table in the sbapi database.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sbapi.app.models.sbapi_sqlalchemy_model_base import Base

if TYPE_CHECKING:
    from sbapi.app.models.sbapi_sqlalchemy_model_characters import Character


class Actor(Base):
    """actors database table model (real-world cast members)"""

    __tablename__ = "actors"
    __table_args__ = (Index("idx_actors", "actor_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_name: Mapped[str] = mapped_column(String(2048), unique=True)
    last_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    character_links: Mapped[list[CharacterActor]] = relationship(
        back_populates="actor", passive_deletes=True
    )


class CharacterActor(Base):
    """character_actors: which actor played or voiced which character"""

    __tablename__ = "character_actors"
    __table_args__ = (
        CheckConstraint("credit_type IN ('live_action', 'voice')"),
        UniqueConstraint("character_id", "actor_id"),
        Index("idx_character_actors_actor_id", "actor_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id", ondelete="CASCADE")
    )
    actor_id: Mapped[int] = mapped_column(ForeignKey("actors.id", ondelete="CASCADE"))
    credit_type: Mapped[str | None] = mapped_column(String(2048))
    notes: Mapped[str | None] = mapped_column(Text)

    character: Mapped[Character] = relationship(back_populates="actor_links")
    actor: Mapped[Actor] = relationship(back_populates="character_links")
