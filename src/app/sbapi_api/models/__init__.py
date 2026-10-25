"""Import every model so they all register on the shared Base.metadata."""
from app.sbapi_api.models.sbapi_sqlalchemy_model_base import Base
from app.sbapi_api.models.sbapi_sqlalchemy_model_media import Episode, Media
from app.sbapi_api.models.sbapi_sqlalchemy_model_actors import Actor, CharacterActor
from app.sbapi_api.models.sbapi_sqlalchemy_model_factions import Faction
from app.sbapi_api.models.sbapi_sqlalchemy_model_locations import Location
from app.sbapi_api.models.sbapi_sqlalchemy_model_characters import Character
from app.sbapi_api.models.sbapi_sqlalchemy_model_vehicles import Vehicle, VehicleCrew
from app.sbapi_api.models.sbapi_sqlalchemy_model_items import Item
from app.sbapi_api.models.sbapi_sqlalchemy_model_quotes import Quote
from app.sbapi_api.models.sbapi_sqlalchemy_model_links import (
    media_characters,
    media_locations,
    media_vehicles,
)
from app.sbapi_api.models.sbapi_sqlalchemy_model_annotations import Citation, Trivia
