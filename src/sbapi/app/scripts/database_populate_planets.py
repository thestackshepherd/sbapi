"""
Script populates the planets table
"""
from datetime import UTC, datetime

from sqlalchemy import select

from sbapi.app.database import SbapiDbConnection
from sbapi.app.models import Planet

planet_spaceball_description = """Home of the Spaceballs. Has squandered its own air,
so it schemes to steal Druidia's atmosphere."""
planet_druidia_description = (
    "Kingdom of King Roland and Princess Vespa. Its fresh air "
    "is protected by a shield (combination 1-2-3-4-5)."
)
moon_of_vega_description = (
    "Desert moon where the heroes crash-land. Home of Yogurt "
    "and the Dinks; where Lone Starr learns the Schwartz."
)
planet_of_the_apes_description = "Where Mega Maid's head crash-lands in the final scene."
space_stop_5_description = "Roadside diner where the heroes stop to eat."

NOW = datetime.now(UTC)
PLANETS = [
    {
        "name": "Planet Spaceball",
        "ruler_id": "skroob",
        "planet_type": "planet",
        "description": planet_spaceball_description,
        "government": "presidency",
        "capital": "Spaceball City",
        "parody_of": "Galactic Empire (Star Wars)",
        "last_updated": NOW,
    },
    {
        "name": "Planet Druidia",
        "ruler_id": "roland",
        "planet_type": "planet",
        "description": planet_druidia_description,
        "government": "monarchy",
        "capital": None,
        "parody_of": "Alderaan (Star Wars)",
        "last_updated": NOW,
    },
    {
        "name": "Moon of Vega",
        "ruler_id": None,  # Yogurt lives here but doesn't rule it
        "planet_type": "moon",
        "description": moon_of_vega_description,
        "government": None,
        "capital": None,
        "parody_of": "Tatooine / Dagobah (Star Wars)",
        "last_updated": NOW,
    },
    {
        "name": "Planet of the Apes",
        "ruler_id": None,
        "planet_type": "planet",
        "description": planet_of_the_apes_description,
        "government": None,
        "capital": None,
        "parody_of": "Planet of the Apes (1968)",
        "last_updated": NOW,
    },
    {
        "name": "Space Stop 5",
        "ruler_id": None,
        "planet_type": "station",
        "description": space_stop_5_description,
        "government": None,
        "capital": None,
        "parody_of": "Alien (chestburster scene)",
        "last_updated": NOW,
    },
]


def main() -> None:
    """
    populate planets table with data defined in the PLANETS var.
    """
    sbapidb_connection = SbapiDbConnection()
    with sbapidb_connection.get_session() as session:
        for row in PLANETS:
            exists = session.scalar(select(Planet).where(Planet.name == row["name"]))
            if exists:
                print(f"skipped {row['name']} (already exists)")
                continue
            session.add(Planet(**row))
            print(f"added {row['name']}")
        session.commit()


if __name__ == "__main__":
    main()
