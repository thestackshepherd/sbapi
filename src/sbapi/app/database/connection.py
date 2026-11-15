"""
application postgresql db connection.
"""

import os

import dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, sessionmaker

dotenv.load_dotenv()


class SbapiDbConnection:
    """session factory
    Any parameter left out falls back to its DATABASE_* environment variable.
    """

    def __init__(
        self,
        db_username: str | None = None,
        db_password: str | None = None,
        db_host: str | None = None,
        db_port: str | int | None = None,
        db_name: str | None = None,
    ) -> None:
        self.db_username = db_username or os.getenv("DATABASE_USERNAME")
        self.db_password = db_password or os.getenv("DATABASE_PASSWORD")
        self.db_host = db_host or os.getenv("DATABASE_HOST")
        self.db_port = db_port or os.getenv("DATABASE_PORT", "5432")
        self.db_name = db_name or os.getenv("DATABASE_NAME")

        missing = [
            env_var
            for env_var, value in (
                ("DATABASE_USERNAME", self.db_username),
                ("DATABASE_HOST", self.db_host),
                ("DATABASE_NAME", self.db_name),
            )
            if not value
        ]
        if missing:
            raise ValueError(f"missing database settings: {', '.join(missing)}")

        self.pgurl = URL.create(
            drivername="postgresql+psycopg",
            username=self.db_username,
            password=self.db_password,
            host=self.db_host,
            port=int(self.db_port),
            database=self.db_name,
        )
        self.engine = create_engine(self.pgurl)
        self._sessionmaker = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        """
        return a new PG DB session, meant to be used as a context manager
        with sbapidb_connection.get_session() as session
        Returns:
            Session: a new session bound to this connection's engine
        """
        return self._sessionmaker()
