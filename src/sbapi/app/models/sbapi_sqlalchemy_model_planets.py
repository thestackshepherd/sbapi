from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Planets(Base):
    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, primary_key=False)
    ruler: Mapped[str] = mapped_column(String, nullable=True)
    affiliation: Mapped[str] = mapped_column(String, nullable=True)
    residents: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    films: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    parody_of: Mapped[str] = mapped_column(String, nullable=True)
    created: Mapped[datetime] = mapped_column(DateTime)
    edited: Mapped[datetime] = mapped_column(DateTime)
    url: Mapped[str] = mapped_column(String, unique=True)
