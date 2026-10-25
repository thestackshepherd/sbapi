from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.sbapi_api.models.sbapi_sqlalchemy_model_base import Base


class Actor(Base):
    """actors database table model (real-world cast members)"""

    __tablename__ = "actors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_name: Mapped[str] = mapped_column(String)
    image_url: Mapped[Optional[str]] = mapped_column(String)
    source_url: Mapped[Optional[str]] = mapped_column(String)
    last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    character_links: Mapped[list["CharacterActor"]] = relationship(back_populates="actor")
    trivia: Mapped[list["Trivia"]] = relationship(foreign_keys="Trivia.actor_id")
    citations: Mapped[list["Citation"]] = relationship(foreign_keys="Citation.actor_id")


class CharacterActor(Base):
    """character_actors: which actor played or voiced which character, per media entry"""

    __tablename__ = "character_actors"
    __table_args__ = (
        CheckConstraint("credit_type IN ('live_action', 'voice')"),
        UniqueConstraint("character_id", "actor_id", "media_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id", ondelete="CASCADE"), index=True
    )
    actor_id: Mapped[int] = mapped_column(
        ForeignKey("actors.id", ondelete="CASCADE"), index=True
    )
    media_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("media.id", ondelete="SET NULL"), index=True
    )
    credit_type: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    character: Mapped["Character"] = relationship(back_populates="actor_links")
    actor: Mapped["Actor"] = relationship(back_populates="character_links")
    media: Mapped[Optional["Media"]] = relationship()
