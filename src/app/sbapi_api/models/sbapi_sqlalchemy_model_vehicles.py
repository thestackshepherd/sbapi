from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.sbapi_api.models.sbapi_sqlalchemy_model_base import Base


class Vehicle(Base):
    """vehicles database table model (Eagle 5, Spaceball One, ...)"""

    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_name: Mapped[str] = mapped_column(String)
    vehicle_type: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    parody_of: Mapped[Optional[str]] = mapped_column(String)
    faction_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("factions.id", ondelete="SET NULL"), index=True
    )
    image_url: Mapped[Optional[str]] = mapped_column(String)
    source_url: Mapped[Optional[str]] = mapped_column(String)
    last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    faction: Mapped[Optional["Faction"]] = relationship(back_populates="vehicles")
    crew: Mapped[list["VehicleCrew"]] = relationship(back_populates="vehicle")
    media: Mapped[list["Media"]] = relationship(
        secondary="media_vehicles", back_populates="vehicles"
    )
    trivia: Mapped[list["Trivia"]] = relationship(foreign_keys="Trivia.vehicle_id")
    citations: Mapped[list["Citation"]] = relationship(foreign_keys="Citation.vehicle_id")


class VehicleCrew(Base):
    """vehicle_crew: who is aboard a vehicle, and in what role"""

    __tablename__ = "vehicle_crew"

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True
    )
    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id", ondelete="CASCADE"), primary_key=True, index=True
    )
    crew_role: Mapped[Optional[str]] = mapped_column(String)

    vehicle: Mapped["Vehicle"] = relationship(back_populates="crew")
    character: Mapped["Character"] = relationship(back_populates="crew_roles")
