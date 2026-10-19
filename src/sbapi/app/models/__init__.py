"""Import every model so they all register on the shared Base.metadata."""
from sbapi.app.models.sbapi_sqlalchemy_model_base import Base
from sbapi.app.models.sbapi_sqlalchemy_model_media import Episode, Media
from sbapi.app.models.sbapi_sqlalchemy_model_actors import Actor, CharacterActor
from sbapi.app.models.sbapi_sqlalchemy_model_factions import Faction
from sbapi.app.models.sbapi_sqlalchemy_model_locations import Location
from sbapi.app.models.sbapi_sqlalchemy_model_characters import Character
from sbapi.app.models.sbapi_sqlalchemy_model_vehicles import Vehicle, VehicleCrew
from sbapi.app.models.sbapi_sqlalchemy_model_items import Item
from sbapi.app.models.sbapi_sqlalchemy_model_quotes import Quote
from sbapi.app.models.sbapi_sqlalchemy_model_links import (
    media_characters,
    media_locations,
    media_vehicles,
)
from sbapi.app.models.sbapi_sqlalchemy_model_annotations import Citation, Trivia
