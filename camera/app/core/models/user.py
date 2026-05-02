"""Model for a user's data."""

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """Model for a user's data gained from the server API.

    Attributes:
        id: A user's ID
        email: Email of the user
        is_admin: A flag for whether the user is an admin
    """

    id: str
    email: str
    is_admin: bool
