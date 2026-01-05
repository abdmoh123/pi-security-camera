"""Module for handling environmental configurations."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

_ = load_dotenv()


def _get_secret() -> str:
    """Loads secret key from environment variables.

    Raises ValueError if the secret key is not set in the environment variables.
    """
    secret = os.getenv("SECRET_KEY")
    if not secret:
        raise ValueError("SECRET_KEY is not set!")
    return secret


@dataclass
class Settings:
    """Centralized settings management for the application."""

    SECRET_KEY: str = _get_secret()  # Generate a random one with `openssl rand -hex 32`
    ALGORITHM: str = "HS256"

    # Token expiry times
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Admin bootstrapping
    # The first registered user will automatically become an admin if this is enabled
    ENABLE_FIRST_USER_ADMIN: bool = os.getenv("ENABLE_FIRST_USER_ADMIN", "true").lower() == "true"


settings = Settings()
