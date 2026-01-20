"""Module for handling environmental configurations."""

import os
from dataclasses import dataclass
from enum import Enum

from dotenv import load_dotenv

_ = load_dotenv()


class DBType(str, Enum):
    """Types of databases that are currently supported."""

    SQLITE = "sqlite"
    POSTGRES = "postgres"


class JWTAlgorithm(str, Enum):
    """Supported JWT encoding algorithms."""

    HS256 = "HS256"


def _get_db_type() -> DBType:
    """Gets the database type from the host's environment variables."""
    # Default to sqlite if undefined
    db_type_env: str = os.getenv("DB_TYPE", "sqlite").lower()
    try:
        return DBType(db_type_env)
    except ValueError:
        raise ValueError(f"Invalid DB type: {db_type_env}")


def _get_db_url(db_type: DBType) -> str:
    """Gets a database URL using the data given in the environment variables."""
    match db_type:
        case DBType.SQLITE:
            return "sqlite:///app.db"
        case DBType.POSTGRES:
            user: str | None = os.getenv("POSTGRES_USER")
            password: str | None = os.getenv("POSTGRES_PASSWORD")
            port: str | None = os.getenv("POSTGRES_PORT")
            db_name: str | None = os.getenv("POSTGRES_DB_NAME")
            host: str | None = os.getenv("POSTGRES_HOST")
            if user is None:
                raise ValueError("Cannot connect to a database! POSTGRES_USER is not set!")
            if password is None:
                raise ValueError("Cannot connect to a database! POSTGRES_PASSWORD is not set!")
            if port is None:
                raise ValueError("Cannot connect to a database! POSTGRES_PORT is not set!")
            if db_name is None:
                raise ValueError("Cannot connect to a database! POSTGRES_DB_NAME is not set!")
            if host is None:
                raise ValueError("Cannot connect to a database! POSTGRES_HOST is not set!")
            return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def _get_secret() -> str:
    """Loads secret key from environment variables.

    Raises ValueError if the secret key is not set in the environment variables.
    """
    secret = os.getenv("SECRET_KEY")
    if not secret:
        raise ValueError("SECRET_KEY is not set!")
    return secret


def _get_jwt_algorithm() -> JWTAlgorithm:
    """Loads JWT algorithm from environment variables.

    Default to HS256 if the environment variable is not set.
    """
    algorithm = os.getenv("JWT_ALGORITHM")
    if not algorithm:
        return JWTAlgorithm.HS256
    return JWTAlgorithm(algorithm)


@dataclass
class Settings:
    """Centralized settings management for the application."""

    DB_TYPE: DBType = _get_db_type()
    DB_URL: str = _get_db_url(DB_TYPE)

    SECRET_KEY: str = _get_secret()  # Generate a random one with `openssl rand -hex 32`
    JWT_ALGORITHM: JWTAlgorithm = _get_jwt_algorithm()  # Default to HS256

    # Token expiry times
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Admin bootstrapping
    # The first registered user will automatically become an admin if this is enabled
    ENABLE_FIRST_USER_ADMIN: bool = os.getenv("ENABLE_FIRST_USER_ADMIN", "true").lower() == "true"


settings = Settings()
