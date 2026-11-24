"""
SQLAlchemy ORM Model file represents the planets table in the sbapi database.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sbapi.app.models.sbapi_sqlalchemy_model_base import Base

if TYPE_CHECKING:
    from sbapi.app.models.sbapi_sqlalchemy_model_annotations import Citation, Trivia
    from sbapi.app.models.sbapi_sqlalchemy_model_characters import Character


class Planet(Base):
    """planets database table model (planets, moons, and stations)"""

    __tablename__ = "planets"
    __table_args__ = (Index("idx_planets", "name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(2048))
    ruler_id: Mapped[str | None] = mapped_column(String(2048))
    planet_type: Mapped[str | None] = mapped_column(String(2048))
    description: Mapped[str | None] = mapped_column(Text)
    government: Mapped[str | None] = mapped_column(String(2048))
    capital: Mapped[str | None] = mapped_column(String(2048))
    parody_of: Mapped[str | None] = mapped_column(String(2048))
    last_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    natives: Mapped[list[Character]] = relationship(
        foreign_keys="Character.homeworld_id", back_populates="homeworld"
    )
    trivia: Mapped[list[Trivia]] = relationship(foreign_keys="Trivia.planet_id")
    citations: Mapped[list[Citation]] = relationship(foreign_keys="Citation.planet_id")
