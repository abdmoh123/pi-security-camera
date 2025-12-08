"""File for connecting the server to the database."""

import os
from collections.abc import Generator
from enum import Enum
from typing import Any, Protocol

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.db_models import Base


class DBType(str, Enum):
    """Types of databases that are currently supported."""

    SQLITE = "sqlite"
    POSTGRES = "postgres"


def get_db_type() -> DBType:
    """Gets the database type from the host's environment variables."""
    # Default to sqlite if undefined
    db_type_env: str = os.getenv("DB_TYPE", "sqlite").lower()
    try:
        return DBType(db_type_env)
    except ValueError:
        raise ValueError(f"Invalid DB type: {db_type_env}")


def get_db_url() -> str:
    """Reads the database url from the host's environment files."""
    match get_db_type():
        case DBType.SQLITE:
            return "sqlite:///app.db"
        case DBType.POSTGRES:
            url: str | None = os.getenv("DATABASE_URL")
            if not url:
                raise ValueError("Cannot connect to a database! DATABASE_URL is not set!")
            return url


class DBConnectorProtocol(Protocol):
    """Protocol for all database connectors used to connect the API to the database."""

    def get_engine(self) -> Engine:
        """Returns the Engine of the database.

        Used to get the sqlalchemy ORM to work.
        """
        ...

    def get_session(self) -> Generator[Session, None, None]:
        """Returns the database session.

        Used when querying the database.
        """
        ...


class GeneralDBConnector:
    """Generalised database connector used to connect the API to the database."""

    def __init__(self, database_url: str, connect_args: dict[str, Any]):  # pyright: ignore[reportExplicitAny]
        """Initialises and sets up the engine and session so the API can interact with the database."""
        self._engine: Engine = create_engine(database_url, connect_args=connect_args)
        self._session_maker: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    def get_engine(self) -> Engine:
        """Returns the Engine of the database.

        Used to get the sqlalchemy ORM to work.
        """
        return self._engine

    def get_session(self) -> Generator[Session, None, None]:
        """Returns the database session.

        Used when querying the database.
        """
        session = self._session_maker()
        try:
            yield session
        finally:
            session.close()


def create_postgres_connector(database_url: str) -> DBConnectorProtocol:
    """Creates a postgres database connector."""
    return GeneralDBConnector(database_url, connect_args={})


def create_sqlite_connector(database_url: str) -> DBConnectorProtocol:
    """Creates a sqlite database connector with some default arguments."""
    return GeneralDBConnector(database_url, connect_args={"check_same_thread": False})


def create_db_connector() -> DBConnectorProtocol:
    """Creates a database connector based on environment variable values."""
    match get_db_type():
        case DBType.SQLITE:
            return create_sqlite_connector(get_db_url())
        case DBType.POSTGRES:
            return create_postgres_connector(get_db_url())


def get_db() -> Generator[Session, None, None]:
    """Returns an instance of the database that you can query against."""
    yield from db_connector.get_session()


db_connector: DBConnectorProtocol = create_db_connector()
Base.metadata.create_all(bind=db_connector.get_engine())
