"""Miscellaneous utility functions."""

from app.api.models.users import IDorEmail
from app.db.db_models import User


def user_matches_id_or_email(id_or_email: IDorEmail, user: User) -> bool:
    """Verifies that the given ID or email matches the user's ID or email."""
    if isinstance(id_or_email.value, int):
        return user.id == int(id_or_email.value)
    else:
        return user.email == id_or_email.value
