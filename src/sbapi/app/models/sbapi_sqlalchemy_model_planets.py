"""
SQLAlchemy ORM Model file represents the planets table in the sbapi database.
"""

from datetime import datetime

from sqlalchemy import DateTime, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from sbapi.app.models.sbapi_sqlalchemy_model_base import Base


class Planet(Base):
    """planets database table model (planets, moons, and stations)"""

    __tablename__ = "planets"
    __table_args__ = (Index("idx_planets", "name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    ruler_id: Mapped[str | None] = mapped_column(String)
    planet_type: Mapped[str | None] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text)
    government: Mapped[str | None] = mapped_column(String)
    capital: Mapped[str | None] = mapped_column(String)
    parody_of: Mapped[str | None] = mapped_column(String)
    last_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
