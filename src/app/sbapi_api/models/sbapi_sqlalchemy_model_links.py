"""Pure many-to-many link tables (no extra columns), used as relationship secondaries."""
from sqlalchemy import Column, ForeignKey, Table

from app.sbapi_api.models.sbapi_sqlalchemy_model_base import Base

media_characters = Table(
    "media_characters",
    Base.metadata,
    Column("media_id", ForeignKey("media.id", ondelete="CASCADE"), primary_key=True),
    Column("character_id", ForeignKey("characters.id", ondelete="CASCADE"), primary_key=True, index=True),
)

media_locations = Table(
    "media_locations",
    Base.metadata,
    Column("media_id", ForeignKey("media.id", ondelete="CASCADE"), primary_key=True),
    Column("location_id", ForeignKey("locations.id", ondelete="CASCADE"), primary_key=True, index=True),
)

media_vehicles = Table(
    "media_vehicles",
    Base.metadata,
    Column("media_id", ForeignKey("media.id", ondelete="CASCADE"), primary_key=True),
    Column("vehicle_id", ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True, index=True),
)
