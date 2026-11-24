"""
SQLAlchemy repository for the vehicles and vehicle_crew tables (ships and crews).

Wraps a Session handed in by the caller and never opens or commits one itself.
Write methods flush so generated ids are available; the caller commits. See
sbapi_sqlalchemy_repo_actors.py for the pattern.
"""

from sqlalchemy.orm import Session


class VehicleRepository:
    """database queries for the vehicles table"""

    def __init__(self, session: Session) -> None:
        self.session = session


class VehicleCrewRepository:
    """database queries for the vehicle_crew table"""

    def __init__(self, session: Session) -> None:
        self.session = session
