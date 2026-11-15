"""
populate the actor table
"""

from datetime import UTC, datetime

from sqlalchemy import select

from sbapi.app.database import SbapiDbConnection
from sbapi.app.models import Actor

ACTORS = [
    {"actor_name": "Mel Brooks", "last_updated": datetime.now(UTC)},
    {"actor_name": "John Candy", "last_updated": datetime.now(UTC)},
    {"actor_name": "Rick Moranis", "last_updated": datetime.now(UTC)},
    {"actor_name": "Bill Pullman", "last_updated": datetime.now(UTC)},
    {"actor_name": "Daphne Zuniga", "last_updated": datetime.now(UTC)},
    {"actor_name": "Dick Van Patten", "last_updated": datetime.now(UTC)},
    {"actor_name": "George Wyner", "last_updated": datetime.now(UTC)},
    {"actor_name": "Michael Winslow", "last_updated": datetime.now(UTC)},
    {"actor_name": "Joan Rivers", "last_updated": datetime.now(UTC)},
    {"actor_name": "Lorene Yarnell", "last_updated": datetime.now(UTC)},
    {"actor_name": "John Hurt", "last_updated": datetime.now(UTC)},
    {"actor_name": "Sal Viscuso", "last_updated": datetime.now(UTC)},
    {"actor_name": "Ronny Graham", "last_updated": datetime.now(UTC)},
    {"actor_name": "Jm J. Bullock", "last_updated": datetime.now(UTC)},
    {"actor_name": "Leslie Bevis", "last_updated": datetime.now(UTC)},
    {"actor_name": "Jim Jackman", "last_updated": datetime.now(UTC)},
    {"actor_name": "Michael Pniewski", "last_updated": datetime.now(UTC)},
    {"actor_name": "Sandy Helberg", "last_updated": datetime.now(UTC)},
    {"actor_name": "Stephen Tobolowsky", "last_updated": datetime.now(UTC)},
    {"actor_name": "Jeff MacGregor", "last_updated": datetime.now(UTC)},
    {"actor_name": "Henry Kaiser", "last_updated": datetime.now(UTC)},
    {"actor_name": "Denise Gallup", "last_updated": datetime.now(UTC)},
    {"actor_name": "Dian Gallup", "last_updated": datetime.now(UTC)},
    {"actor_name": "Gail Barle", "last_updated": datetime.now(UTC)},
    {"actor_name": "Dey Young", "last_updated": datetime.now(UTC)},
    {"actor_name": "Rhonda Shear", "last_updated": datetime.now(UTC)},
    {"actor_name": "Robert Prescott", "last_updated": datetime.now(UTC)},
    {"actor_name": "Jack Riley", "last_updated": datetime.now(UTC)},
    {"actor_name": "Tom Dressen", "last_updated": datetime.now(UTC)},
    {"actor_name": "Rudy DeLuca", "last_updated": datetime.now(UTC)},
    {"actor_name": "Tony Griffin", "last_updated": datetime.now(UTC)},
    {"actor_name": "Rick Ducommun", "last_updated": datetime.now(UTC)},
    {"actor_name": "Ken Olfson", "last_updated": datetime.now(UTC)},
    {"actor_name": "Bryan O'Berne", "last_updated": datetime.now(UTC)},
    {"actor_name": "Wayne Wilson", "last_updated": datetime.now(UTC)},
    {"actor_name": "Ira Miller", "last_updated": datetime.now(UTC)},
    {"actor_name": "Earl Finn", "last_updated": datetime.now(UTC)},
    {"actor_name": "Mitchell Bock", "last_updated": datetime.now(UTC)},
    {"actor_name": "Tommy Swerdlow", "last_updated": datetime.now(UTC)},
    {"actor_name": "Tim Russ", "last_updated": datetime.now(UTC)},
    {"actor_name": "Ed Gale", "last_updated": datetime.now(UTC)},
    {"actor_name": "Antonio Hoyos", "last_updated": datetime.now(UTC)},
    {"actor_name": "Felix Silla", "last_updated": datetime.now(UTC)},
    {"actor_name": "Arturo Gil", "last_updated": datetime.now(UTC)},
    {"actor_name": "Tony Cox", "last_updated": datetime.now(UTC)},
    {"actor_name": "John Kennedy Hayden", "last_updated": datetime.now(UTC)},
    {"actor_name": "Deanna Booher", "last_updated": datetime.now(UTC)},
    {"actor_name": "Johnny Silver", "last_updated": datetime.now(UTC)},
    {"actor_name": "Brenda Strong", "last_updated": datetime.now(UTC)},
    {"actor_name": "Dom DeLuise", "last_updated": datetime.now(UTC)},
]

def main() -> None:
    """
    populate actor table with data defined in the ACTORS var.
    """
    sbapidb_connection = SbapiDbConnection()
    with sbapidb_connection.get_session() as session:
        for row in ACTORS:
            exists = session.scalar(
                select(Actor).where(Actor.actor_name == row["actor_name"])
            )
            if exists:
                continue
            session.add(Actor(**row, last_updated=datetime.now(UTC)))
        session.commit()


if __name__ == "__main__":
    main()
