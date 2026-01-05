"""Module for handling environmental configurations."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

_ = load_dotenv()


@dataclass
class Settings:
    """Centralized settings management for the application."""

    # Admin bootstrapping
    # The first registered user will automatically become an admin if this is enabled
    ENABLE_FIRST_USER_ADMIN: bool = os.getenv("ENABLE_FIRST_USER_ADMIN", "true").lower() == "true"


settings = Settings()
