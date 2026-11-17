"""
Populate the sbapi database.

All populating logic lives here. The data being inserted is defined in the
database_populate_<table>.py modules. Link and annotation rows reference other
rows by natural key (character_name, actor_name, vehicle_name, ...) and the ids
are looked up here at insert time.
"""

from sqlalchemy import select

from sbapi.app.database import SbapiDbConnection
from sbapi.app.models import (
    Actor,
    Character,
    CharacterActor,
    Citation,
    Item,
    Planet,
    Quote,
    Trivia,
    Vehicle,
    VehicleCrew,
)
from sbapi.app.scripts.database_populate_actors import ACTORS
from sbapi.app.scripts.database_populate_character_actors import CHARACTER_ACTORS
from sbapi.app.scripts.database_populate_characters import CHARACTERS
from sbapi.app.scripts.database_populate_citations import CITATIONS
from sbapi.app.scripts.database_populate_items import ITEMS
from sbapi.app.scripts.database_populate_planets import PLANETS
from sbapi.app.scripts.database_populate_quotes import QUOTES
from sbapi.app.scripts.database_populate_trivia import TRIVIA
from sbapi.app.scripts.database_populate_vehicle_crew import VEHICLE_CREW
from sbapi.app.scripts.database_populate_vehicles import VEHICLES

# natural key used in the data modules -> (lookup column, FK column it fills).
# trivia and citations rows name exactly one of these.
ENTITY_KEYS = {
    "character_name": (Character.character_name, "character_id"),
    "planet_name": (Planet.name, "planet_id"),
    "vehicle_name": (Vehicle.vehicle_name, "vehicle_id"),
    "item_name": (Item.item_name, "item_id"),
    "actor_name": (Actor.actor_name, "actor_id"),
    "quote_text": (Quote.quote_text, "quote_id"),
}


def lookup_id(session, column, value) -> int | None:
    """
    return the id of the row whose column equals value, or None if missing.
    """
    model = column.class_
    return session.scalar(select(model.id).where(column == value).limit(1))


def populate_planets(sbapidb_connection: SbapiDbConnection) -> None:
    """
    populate planets table with data defined in the PLANETS var.
    """
    with sbapidb_connection.get_session() as session:
        for row in PLANETS:
            exists = session.scalar(select(Planet).where(Planet.name == row["name"]))
            if exists:
                print(f"skipped {row['name']} (already exists)")
                continue
            session.add(Planet(**row))
            print(f"added {row['name']}")
        session.commit()


def populate_actors(sbapidb_connection: SbapiDbConnection) -> None:
    """
    populate actor table with data defined in the ACTORS var.
    """
    with sbapidb_connection.get_session() as session:
        for row in ACTORS:
            exists = session.scalar(
                select(Actor).where(Actor.actor_name == row["actor_name"])
            )
            if not exists:
                session.add(Actor(**row))
            else:
                continue
        session.commit()


def populate_characters(sbapidb_connection: SbapiDbConnection) -> None:
    """
    populate characters table with data defined in the CHARACTERS var.
    """
    with sbapidb_connection.get_session() as session:
        for row in CHARACTERS:
            exists = session.scalar(
                select(Character).where(
                    Character.character_name == row["character_name"]
                )
            )
            if exists:
                print(f"skipped {row['character_name']} (already exists)")
                continue
            session.add(Character(**row))
            print(f"added {row['character_name']}")
        session.commit()


def populate_vehicles(sbapidb_connection: SbapiDbConnection) -> None:
    """
    populate vehicles table with data defined in the VEHICLES var.
    """
    with sbapidb_connection.get_session() as session:
        for row in VEHICLES:
            exists = session.scalar(
                select(Vehicle).where(Vehicle.vehicle_name == row["vehicle_name"])
            )
            if exists:
                print(f"skipped {row['vehicle_name']} (already exists)")
                continue
            session.add(Vehicle(**row))
            print(f"added {row['vehicle_name']}")
        session.commit()


def populate_items(sbapidb_connection: SbapiDbConnection) -> None:
    """
    populate items table with data defined in the ITEMS var.
    owner_character_name is resolved to owner_character_id.
    """
    with sbapidb_connection.get_session() as session:
        for row in ITEMS:
            exists = session.scalar(
                select(Item).where(Item.item_name == row["item_name"])
            )
            if exists:
                print(f"skipped {row['item_name']} (already exists)")
                continue
            data = dict(row)
            owner_name = data.pop("owner_character_name")
            data["owner_character_id"] = None
            if owner_name:
                data["owner_character_id"] = lookup_id(
                    session, Character.character_name, owner_name
                )
                if data["owner_character_id"] is None:
                    print(f"warning: owner {owner_name} not found for "
                          f"{row['item_name']}, leaving owner empty")
            session.add(Item(**data))
            print(f"added {row['item_name']}")
        session.commit()


def populate_quotes(sbapidb_connection: SbapiDbConnection) -> None:
    """
    populate quotes table with data defined in the QUOTES var.
    character_name is resolved to character_id.
    """
    with sbapidb_connection.get_session() as session:
        for row in QUOTES:
            exists = session.scalar(
                select(Quote).where(Quote.quote_text == row["quote_text"])
            )
            if exists:
                print(f"skipped quote {row['quote_text'][:40]!r} (already exists)")
                continue
            data = dict(row)
            character_name = data.pop("character_name")
            data["character_id"] = None
            if character_name:
                data["character_id"] = lookup_id(
                    session, Character.character_name, character_name
                )
                if data["character_id"] is None:
                    print(f"warning: character {character_name} not found, "
                          f"skipped quote {row['quote_text'][:40]!r}")
                    continue
            session.add(Quote(**data))
            print(f"added quote {row['quote_text'][:40]!r}")
        session.commit()


def populate_character_actors(sbapidb_connection: SbapiDbConnection) -> None:
    """
    populate character_actors table with data defined in the CHARACTER_ACTORS var.
    """
    with sbapidb_connection.get_session() as session:
        for row in CHARACTER_ACTORS:
            label = f"{row['character_name']} / {row['actor_name']}"
            character_id = lookup_id(
                session, Character.character_name, row["character_name"]
            )
            actor_id = lookup_id(session, Actor.actor_name, row["actor_name"])
            if character_id is None or actor_id is None:
                print(f"warning: skipped {label} (character or actor not found)")
                continue
            exists = session.scalar(
                select(CharacterActor).where(
                    CharacterActor.character_id == character_id,
                    CharacterActor.actor_id == actor_id,
                )
            )
            if exists:
                print(f"skipped {label} (already exists)")
                continue
            session.add(
                CharacterActor(
                    character_id=character_id,
                    actor_id=actor_id,
                    credit_type=row["credit_type"],
                    notes=row["notes"],
                )
            )
            print(f"added {label}")
        session.commit()


def populate_vehicle_crew(sbapidb_connection: SbapiDbConnection) -> None:
    """
    populate vehicle_crew table with data defined in the VEHICLE_CREW var.
    """
    with sbapidb_connection.get_session() as session:
        for row in VEHICLE_CREW:
            label = f"{row['vehicle_name']} / {row['character_name']}"
            vehicle_id = lookup_id(session, Vehicle.vehicle_name, row["vehicle_name"])
            character_id = lookup_id(
                session, Character.character_name, row["character_name"]
            )
            if vehicle_id is None or character_id is None:
                print(f"warning: skipped {label} (vehicle or character not found)")
                continue
            exists = session.get(VehicleCrew, (vehicle_id, character_id))
            if exists:
                print(f"skipped {label} (already exists)")
                continue
            session.add(
                VehicleCrew(
                    vehicle_id=vehicle_id,
                    character_id=character_id,
                    crew_role=row["crew_role"],
                )
            )
            print(f"added {label}")
        session.commit()


def resolve_entity(session, row: dict) -> tuple[str, str, int | None]:
    """
    find the one natural key in a trivia/citations row and look up its id.
    returns (key name, FK column name, id or None).
    """
    keys = [key for key in ENTITY_KEYS if key in row]
    if len(keys) != 1:
        raise ValueError(f"row must name exactly one entity: {row}")
    column, fk_column = ENTITY_KEYS[keys[0]]
    return keys[0], fk_column, lookup_id(session, column, row[keys[0]])


def populate_trivia(sbapidb_connection: SbapiDbConnection) -> None:
    """
    populate trivia table with data defined in the TRIVIA var.
    """
    with sbapidb_connection.get_session() as session:
        for row in TRIVIA:
            key, fk_column, entity_id = resolve_entity(session, row)
            label = f"trivia for {row[key]} {row['trivia_text'][:40]!r}"
            if entity_id is None:
                print(f"warning: skipped {label} ({row[key]} not found)")
                continue
            exists = session.scalar(
                select(Trivia).where(
                    getattr(Trivia, fk_column) == entity_id,
                    Trivia.trivia_text == row["trivia_text"],
                )
            )
            if exists:
                print(f"skipped {label} (already exists)")
                continue
            session.add(
                Trivia(
                    trivia_kind=row["trivia_kind"],
                    trivia_text=row["trivia_text"],
                    **{fk_column: entity_id},
                )
            )
            print(f"added {label}")
        session.commit()


def populate_citations(sbapidb_connection: SbapiDbConnection) -> None:
    """
    populate citations table with data defined in the CITATIONS var.
    """
    with sbapidb_connection.get_session() as session:
        for row in CITATIONS:
            key, fk_column, entity_id = resolve_entity(session, row)
            label = f"citation {row['citation_number']} for {row[key]}"
            if entity_id is None:
                print(f"warning: skipped {label} ({row[key]} not found)")
                continue
            exists = session.scalar(
                select(Citation).where(
                    getattr(Citation, fk_column) == entity_id,
                    Citation.citation_number == row["citation_number"],
                    Citation.source_text == row["source_text"],
                )
            )
            if exists:
                print(f"skipped {label} (already exists)")
                continue
            session.add(
                Citation(
                    citation_number=row["citation_number"],
                    source_text=row["source_text"],
                    source_url=row["source_url"],
                    **{fk_column: entity_id},
                )
            )
            print(f"added {label}")
        session.commit()


def main() -> None:
    """
    populate every table in FK-safe order: planets before characters, every
    entity table before the link (character_actors, vehicle_crew) and
    annotation (trivia, citations) tables that reference them.
    """
    sbapidb_connection = SbapiDbConnection()
    populate_planets(sbapidb_connection)
    populate_actors(sbapidb_connection)
    populate_characters(sbapidb_connection)
    populate_vehicles(sbapidb_connection)
    populate_items(sbapidb_connection)
    populate_quotes(sbapidb_connection)
    populate_character_actors(sbapidb_connection)
    populate_vehicle_crew(sbapidb_connection)
    populate_trivia(sbapidb_connection)
    populate_citations(sbapidb_connection)


if __name__ == "__main__":
    main()
