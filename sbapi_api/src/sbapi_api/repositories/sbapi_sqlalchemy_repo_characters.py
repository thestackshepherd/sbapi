from sqlalchemy import select
from sqlalchemy.orm import Session

from sbapi_api.models import Character


class CharacterRepository:
    """read access to the characters table"""

    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> list[Character]:
        return list(self.session.scalars(select(Character).order_by(Character.id)))
