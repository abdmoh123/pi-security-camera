"""Model for a user's data."""

from dataclasses import dataclass


@dataclass
class User:
    """Model for a user's data."""

    id: str
    email: str
    is_admin: bool

