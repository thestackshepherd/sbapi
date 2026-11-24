"""
SQLAlchemy repository for the characters table (characters in the film).

Wraps a Session handed in by the caller and never opens or commits one itself.
Write methods flush so generated ids are available; the caller commits. See
sbapi_sqlalchemy_repo_actors.py for the pattern.
"""

from sqlalchemy.orm import Session

from sbapi.app.models import Character


class CharacterRepository:
    """database queries for the characters table"""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_character_by_id(self, character_id: int) -> Character | None:
        """get a character by id"""
        return self.session.get(Character, character_id)

    def get_character_by_name(self, character_name: str) -> Character | None:
        """get a character by name"""
        return self.session.get(Character, character_name)
