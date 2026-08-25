from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Faction(Base):
    __tablename__ = "faction"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    leader: Mapped[str] = mapped_column(String, nullable=True)
    homeworld: Mapped[str] = mapped_column(String, nullable=True)
    members: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    parody_of: Mapped[str] = mapped_column(String, nullable=True)
    films: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    created: Mapped[datetime] = mapped_column(DateTime)
    edited: Mapped[datetime] = mapped_column(DateTime)
    url: Mapped[str] = mapped_column(String, unique=True)
