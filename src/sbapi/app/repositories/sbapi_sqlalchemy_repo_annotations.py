"""
SQLAlchemy repository for the trivia and citations tables (notes and sources).

Wraps a Session handed in by the caller and never opens or commits one itself.
Write methods flush so generated ids are available; the caller commits. See
sbapi_sqlalchemy_repo_actors.py for the pattern.
"""

from sqlalchemy.orm import Session


class CitationRepository:
    """database queries for the citations table"""

    def __init__(self, session: Session) -> None:
        self.session = session


class TriviaRepository:
    """database queries for the trivia table"""

    def __init__(self, session: Session) -> None:
        self.session = session
