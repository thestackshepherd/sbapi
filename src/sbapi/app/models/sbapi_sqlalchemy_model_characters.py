from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sbapi.app.models.sbapi_sqlalchemy_model_base import Base


class Character(Base):
    """characters database table model"""

    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_name: Mapped[str] = mapped_column(String)
    full_name: Mapped[str | None] = mapped_column(String)
    species: Mapped[str | None] = mapped_column(String)
    gender: Mapped[str | None] = mapped_column(String)
    character_role: Mapped[str | None] = mapped_column(String)
    parody_of: Mapped[str | None] = mapped_column(String)
    faction_id: Mapped[int | None] = mapped_column(
        ForeignKey("factions.id", ondelete="SET NULL")
    )
    homeworld_id: Mapped[int | None] = mapped_column(
        ForeignKey("locations.id", ondelete="SET NULL")
    )
    image_url: Mapped[str | None] = mapped_column(String)
    source_url: Mapped[str | None] = mapped_column(String)
    last_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    faction: Mapped[Faction | None] = relationship(
        foreign_keys=[faction_id], back_populates="members"
    )
    homeworld: Mapped[Location | None] = relationship(
        foreign_keys=[homeworld_id], back_populates="natives"
    )
    actor_links: Mapped[list[CharacterActor]] = relationship(back_populates="character")
    crew_roles: Mapped[list[VehicleCrew]] = relationship(back_populates="character")
    quotes: Mapped[list[Quote]] = relationship(back_populates="character")
    items: Mapped[list[Item]] = relationship(back_populates="owner")
    trivia: Mapped[list[Trivia]] = relationship(foreign_keys="Trivia.character_id")
    citations: Mapped[list[Citation]] = relationship(foreign_keys="Citation.character_id")
