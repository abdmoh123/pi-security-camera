"""Collection of validation functions for user accounts."""

import re

from app.core.validation.regex import email_regex


def password_validator(value: str) -> str:
    """Validates the password. Regex wasn't used because pydantic doesn't support lookaheads.

    Passwords must be have the following:
    - At least 8 characters
    - At least 1 upper and 1 lower case letter
    - At least 1 number
    - At least 1 special character (one of these: @$!%*?&)
    """
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not re.search("[A-Z]", value):
        raise ValueError("Password must contain at least 1 uppercase letter")
    if not re.search("[a-z]", value):
        raise ValueError("Password must contain at least 1 lowercase letter")
    if not re.search("[0-9]", value):
        raise ValueError("Password must contain at least 1 number")
    if not re.search("[@$!%*?&]", value):
        raise ValueError("Password must contain at least 1 special character (one of these: @$!%*?&)")
    return value


def id_or_email_validator(value: str | int) -> int | str:
    """Validates the user ID or email."""
    if isinstance(value, int):  # ID validation
        if value < 1:
            raise ValueError("Invalid ID! Must be at least 1")
        return value
    else:  # Email validation
        if not re.match(email_regex, value):
            raise ValueError("Invalid email! Must follow standard email pattern (e.g. abc@example.com)")
        return value
