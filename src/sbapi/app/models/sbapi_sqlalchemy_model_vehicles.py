from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sbapi.app.models.sbapi_sqlalchemy_model_base import Base


class Vehicle(Base):
    """vehicles database table model (Eagle 5, Spaceball One, ...)"""

    __tablename__ = "vehicles"
    __table_args__ = (Index("idx_vehicles_name", "vehicle_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_name: Mapped[str] = mapped_column(String(2048))
    vehicle_type: Mapped[Optional[str]] = mapped_column(String(2048))
    description: Mapped[Optional[str]] = mapped_column(Text)
    parody_of: Mapped[Optional[str]] = mapped_column(String(2048))
    image_url: Mapped[Optional[str]] = mapped_column(String(2048))
    source_url: Mapped[Optional[str]] = mapped_column(String(2048))
    last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    crew: Mapped[list["VehicleCrew"]] = relationship(back_populates="vehicle")
    trivia: Mapped[list["Trivia"]] = relationship(foreign_keys="Trivia.vehicle_id")
    citations: Mapped[list["Citation"]] = relationship(
        foreign_keys="Citation.vehicle_id"
    )


class VehicleCrew(Base):
    """vehicle_crew: who is aboard a vehicle, and in what role"""

    __tablename__ = "vehicle_crew"
    __table_args__ = (Index("idx_vehicle_crew_character_id", "character_id"),)

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True
    )
    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id", ondelete="CASCADE"), primary_key=True
    )
    crew_role: Mapped[Optional[str]] = mapped_column(String(2048))

    vehicle: Mapped["Vehicle"] = relationship(back_populates="crew")
    character: Mapped["Character"] = relationship(back_populates="crew_roles")
