"""Import every model so they all register on the shared Base.metadata."""
from sbapi_api.models.sbapi_sqlalchemy_model_base import Base
from sbapi_api.models.sbapi_sqlalchemy_model_media import Episode, Media
from sbapi_api.models.sbapi_sqlalchemy_model_actors import Actor, CharacterActor
from sbapi_api.models.sbapi_sqlalchemy_model_factions import Faction
from sbapi_api.models.sbapi_sqlalchemy_model_locations import Location
from sbapi_api.models.sbapi_sqlalchemy_model_characters import Character
from sbapi_api.models.sbapi_sqlalchemy_model_vehicles import Vehicle, VehicleCrew
from sbapi_api.models.sbapi_sqlalchemy_model_items import Item
from sbapi_api.models.sbapi_sqlalchemy_model_quotes import Quote
from sbapi_api.models.sbapi_sqlalchemy_model_links import (
    media_characters,
    media_locations,
    media_vehicles,
)
from sbapi_api.models.sbapi_sqlalchemy_model_annotations import Citation, Trivia
