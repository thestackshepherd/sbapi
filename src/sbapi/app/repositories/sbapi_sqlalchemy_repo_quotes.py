"""
SQLAlchemy repository for the quotes table (lines of dialogue).

Wraps a Session handed in by the caller and never opens or commits one itself.
Write methods flush so generated ids are available; the caller commits. See
sbapi_sqlalchemy_repo_actors.py for the pattern.
"""

from sqlalchemy.orm import Session


class QuoteRepository:
    """database queries for the quotes table"""

    def __init__(self, session: Session) -> None:
        self.session = session
