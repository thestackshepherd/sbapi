"""
sbapi repository module.
"""

from sbapi.app.repositories.sbapi_sqlalchemy_repo_actors import ActorRepository
from sbapi.app.repositories.sbapi_sqlalchemy_repo_characters import CharacterRepository
from sbapi.app.repositories.sbapi_sqlalchemy_repo_items import ItemRepository
from sbapi.app.repositories.sbapi_sqlalchemy_repo_planets import PlanetRepository
from sbapi.app.repositories.sbapi_sqlalchemy_repo_quotes import QuoteRepository
from sbapi.app.repositories.sbapi_sqlalchemy_repo_vehicles import VehicleRepository

__all__ = [
    "ActorRepository",
    "CharacterRepository",
    "ItemRepository",
    "PlanetRepository",
    "QuoteRepository",
    "VehicleRepository",
]
