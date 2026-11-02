from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sbapi.app.models.sbapi_sqlalchemy_model_base import Base


class Location(Base):
    """locations database table model (planets, moons, ships used as settings, ...)"""

    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    location_type: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    parody_of: Mapped[Optional[str]] = mapped_column(String)
    image_url: Mapped[Optional[str]] = mapped_column(String)
    source_url: Mapped[Optional[str]] = mapped_column(String)
    last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    natives: Mapped[list["Character"]] = relationship(
        foreign_keys="Character.homeworld_id", back_populates="homeworld"
    )
    trivia: Mapped[list["Trivia"]] = relationship(foreign_keys="Trivia.location_id")
    citations: Mapped[list["Citation"]] = relationship(foreign_keys="Citation.location_id")
