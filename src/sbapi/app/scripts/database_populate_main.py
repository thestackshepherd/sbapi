"""
Populate the sbapi database.

All populating logic lives here. The data being inserted is defined in the
database_populate_{planets,actors,characters}.py modules.
"""

from sqlalchemy import select

from sbapi.app.database import SbapiDbConnection
from sbapi.app.models import Actor, Character, Planet
from sbapi.app.scripts.database_populate_actors import ACTORS
from sbapi.app.scripts.database_populate_characters import CHARACTERS
from sbapi.app.scripts.database_populate_planets import PLANETS


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


def main() -> None:
    """
    populate every table. planets run first since characters reference them.
    """
    sbapidb_connection = SbapiDbConnection()
    populate_planets(sbapidb_connection)
    populate_actors(sbapidb_connection)
    populate_characters(sbapidb_connection)


if __name__ == "__main__":
    main()
