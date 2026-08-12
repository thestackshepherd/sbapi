from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class People(Base):
    """people database table model"""
    __tablename__ = 'people'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    height: Mapped[str] = mapped_column(String, nullable=True)
    mass: Mapped[str] = mapped_column(String, nullable=True)
    hair_color: Mapped[str] = mapped_column(String, nullable=True)
    skin_color: Mapped[str] = mapped_column(String, nullable=True)
    eye_color: Mapped[str] = mapped_column(String, nullable=True)
    gender: Mapped[str] = mapped_column(String, nullable=True)
    homeworld: Mapped[str] = mapped_column(String, nullable=True)
    films: Mapped[list[str]] = mapped_column(ARRAY(String))
    species: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    vehicles: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    starships: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    parody_of: Mapped[str] = mapped_column(String, nullable=True)
    catchphrases: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    affiliation: Mapped[str] = mapped_column(String, nullable=True)
    occupation: Mapped[str] = mapped_column(String, nullable=True)
    actor: Mapped[str] = mapped_column(String, nullable=True)
    voice_actor: Mapped[str] = mapped_column(String, nullable=True)
    relations: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    first_appearance: Mapped[str] = mapped_column(String, nullable=True)
    last_appearance: Mapped[str] = mapped_column(String, nullable=True)
    created: Mapped[datetime] = mapped_column(DateTime)
    edited: Mapped[datetime] = mapped_column(DateTime)
    url: Mapped[str] = mapped_column(String, unique=True)