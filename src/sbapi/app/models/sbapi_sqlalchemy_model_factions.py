from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sbapi.app.models.sbapi_sqlalchemy_model_base import Base


class Faction(Base):
    """factions database table model"""

    __tablename__ = "factions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    faction_name: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    parody_of: Mapped[Optional[str]] = mapped_column(String)
    image_url: Mapped[Optional[str]] = mapped_column(String)
    source_url: Mapped[Optional[str]] = mapped_column(String)
    last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    members: Mapped[list["Character"]] = relationship(
        foreign_keys="Character.faction_id", back_populates="faction"
    )
    vehicles: Mapped[list["Vehicle"]] = relationship(back_populates="faction")
    trivia: Mapped[list["Trivia"]] = relationship(foreign_keys="Trivia.faction_id")
    citations: Mapped[list["Citation"]] = relationship(foreign_keys="Citation.faction_id")
