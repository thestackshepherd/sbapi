"""
SQLAlchemy repository for the actors table (real-world cast members).

The repository wraps a Session handed in by the caller and never opens or
commits one itself. Write methods flush so generated ids are available, and the
caller decides when to commit:

    with sbapidb_connection.get_session() as session:
        repo = ActorRepository(session)
        repo.create("Mel Brooks")
        session.commit()
"""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from sbapi.app.models import Actor


class ActorRepository:
    """database queries for the actors table"""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, actor_id: int) -> Actor | None:
        """
        return the actor with this id, or None if missing.
        """
        return self.session.get(Actor, actor_id)

    def get_by_name(self, actor_name: str) -> Actor | None:
        """
        return the actor with this exact actor_name, or None if missing.
        """
        return self.session.scalar(select(Actor).where(Actor.actor_name == actor_name))

    def list(self, limit: int = 100, offset: int = 0) -> list[Actor]:
        """
        return a page of actors ordered by actor_name.
        """
        stmt = select(Actor).order_by(Actor.actor_name).limit(limit).offset(offset)
        return list(self.session.scalars(stmt))

    def create(self, actor_name: str) -> Actor:
        """
        add a new actor and flush so its id is populated.
        """
        actor = Actor(actor_name=actor_name, last_updated=datetime.now(UTC))
        self.session.add(actor)
        self.session.flush()
        return actor

    def update(self, actor_id: int, actor_name: str) -> Actor | None:
        """
        rename an actor. returns the updated actor, or None if missing.
        """
        actor = self.get_by_id(actor_id)
        if actor is None:
            return None
        actor.actor_name = actor_name
        actor.last_updated = datetime.now(UTC)
        self.session.flush()
        return actor

    def delete(self, actor_id: int) -> bool:
        """
        delete an actor. returns True if a row was deleted, False if missing.
        """
        actor = self.get_by_id(actor_id)
        if actor is None:
            return False
        self.session.delete(actor)
        self.session.flush()
        return True
