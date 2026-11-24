from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sbapi.app.models.sbapi_sqlalchemy_model_base import Base

if TYPE_CHECKING:
    from sbapi.app.models.sbapi_sqlalchemy_model_actors import CharacterActor
    from sbapi.app.models.sbapi_sqlalchemy_model_annotations import Citation, Trivia
    from sbapi.app.models.sbapi_sqlalchemy_model_items import Item
    from sbapi.app.models.sbapi_sqlalchemy_model_planets import Planet
    from sbapi.app.models.sbapi_sqlalchemy_model_quotes import Quote
    from sbapi.app.models.sbapi_sqlalchemy_model_vehicles import VehicleCrew


class Character(Base):
    """characters database table model"""

    __tablename__ = "characters"
    __table_args__ = (
        Index("idx_characters_name", "character_name"),
        Index("idx_characters_homeworld_id", "homeworld_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_name: Mapped[str] = mapped_column(String(2048))
    full_name: Mapped[str | None] = mapped_column(String(2048))
    species: Mapped[str | None] = mapped_column(String(2048))
    gender: Mapped[str | None] = mapped_column(String(2048))
    character_role: Mapped[str | None] = mapped_column(String(2048))
    parody_of: Mapped[str | None] = mapped_column(String(2048))
    homeworld_id: Mapped[int | None] = mapped_column(
        ForeignKey("planets.id", ondelete="SET NULL")
    )
    image_url: Mapped[str | None] = mapped_column(String(2048))
    source_url: Mapped[str | None] = mapped_column(String(2048))
    last_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    homeworld: Mapped[Planet | None] = relationship(
        foreign_keys=[homeworld_id], back_populates="natives"
    )
    actor_links: Mapped[list[CharacterActor]] = relationship(
        back_populates="character", passive_deletes=True
    )
    crew_roles: Mapped[list[VehicleCrew]] = relationship(
        back_populates="character", passive_deletes=True
    )
    quotes: Mapped[list[Quote]] = relationship(
        back_populates="character", passive_deletes=True
    )
    items: Mapped[list[Item]] = relationship(
        back_populates="owner", passive_deletes=True
    )
    trivia: Mapped[list[Trivia]] = relationship(
        foreign_keys="Trivia.character_id", passive_deletes=True
    )
    citations: Mapped[list[Citation]] = relationship(
        foreign_keys="Citation.character_id", passive_deletes=True
    )
