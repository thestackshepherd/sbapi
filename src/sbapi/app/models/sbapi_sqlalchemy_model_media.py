from datetime import date, datetime
from typing import Optional

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sbapi.app.models.sbapi_sqlalchemy_model_base import Base


class Media(Base):
    """media database table model (one row per film/show)"""

    __tablename__ = "media"
    __table_args__ = (CheckConstraint("media_type IN ('film', 'series')"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    media_type: Mapped[Optional[str]] = mapped_column(String)
    release_date: Mapped[Optional[date]] = mapped_column(Date)
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_url: Mapped[Optional[str]] = mapped_column(String)
    source_url: Mapped[Optional[str]] = mapped_column(String)
    last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    episodes: Mapped[list["Episode"]] = relationship(back_populates="media")
    characters: Mapped[list["Character"]] = relationship(
        secondary="media_characters", back_populates="media"
    )
    locations: Mapped[list["Location"]] = relationship(
        secondary="media_locations", back_populates="media"
    )
    vehicles: Mapped[list["Vehicle"]] = relationship(
        secondary="media_vehicles", back_populates="media"
    )
    trivia: Mapped[list["Trivia"]] = relationship(foreign_keys="Trivia.media_id")
    citations: Mapped[list["Citation"]] = relationship(foreign_keys="Citation.media_id")


class Episode(Base):
    """episodes database table model"""

    __tablename__ = "episodes"
    __table_args__ = (UniqueConstraint("media_id", "season_number", "episode_number"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    media_id: Mapped[int] = mapped_column(
        ForeignKey("media.id", ondelete="CASCADE"), index=True
    )
    season_number: Mapped[Optional[int]] = mapped_column(Integer)
    episode_number: Mapped[Optional[int]] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    air_date: Mapped[Optional[date]] = mapped_column(Date)
    source_url: Mapped[Optional[str]] = mapped_column(String)
    last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    media: Mapped["Media"] = relationship(back_populates="episodes")
    trivia: Mapped[list["Trivia"]] = relationship(foreign_keys="Trivia.episode_id")
    citations: Mapped[list["Citation"]] = relationship(foreign_keys="Citation.episode_id")
