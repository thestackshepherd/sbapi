from flask import Blueprint, jsonify

from sbapi_api.database.connection import SessionLocal
from sbapi_api.models import Character
from sbapi_api.repositories.sbapi_sqlalchemy_repo_characters import CharacterRepository

characters_bp = Blueprint("characters", __name__, url_prefix="/characters")


def serialize_character(character: Character) -> dict:
    return {
        "id": character.id,
        "character_name": character.character_name,
        "full_name": character.full_name,
        "species": character.species,
        "gender": character.gender,
        "character_role": character.character_role,
        "parody_of": character.parody_of,
        "faction_id": character.faction_id,
        "homeworld_id": character.homeworld_id,
        "image_url": character.image_url,
        "source_url": character.source_url,
        "last_updated": character.last_updated.isoformat() if character.last_updated else None,
    }


@characters_bp.get("")
def list_characters():
    with SessionLocal() as session:
        characters = CharacterRepository(session).list_all()
        return jsonify([serialize_character(c) for c in characters])
