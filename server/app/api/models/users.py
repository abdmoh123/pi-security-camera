"""File containing pydantic models for user data."""

import re

from pydantic import BaseModel, Field, field_validator

from app.core.validation.regex import email_regex, password_regex


class IDorEmail(BaseModel):
    """ID or email pydantic model used for special validation."""

    value: int | str

    @field_validator("value", mode="before")
    @classmethod
    def validate_id_or_email(cls, value: int | str) -> int | str:
        """Validates the user ID or email."""
        if isinstance(value, int):  # ID validation
            if value < 1:
                raise ValueError("Invalid ID! Must be at least 1")
            return value
        else:  # Email validation
            if not re.match(email_regex, value):
                raise ValueError("Invalid email! Must follow standard email pattern (e.g. abc@example.com)")
            return value


class User(BaseModel):
    """Base User record/model."""

    id: int = Field(ge=1)
    email: str = Field(pattern=email_regex)  # Rudimentary validation (won't check if email exists)
    password: str = Field(pattern=password_regex, min_length=8)  # Password rules can't apply here as it is a hash

    class Config:
        """Config subclass of User."""

        from_attributes: bool = True


class UserCreate(BaseModel):
    """Request body input as a class for creating a new user."""

    email: str = Field(pattern=email_regex)
    password: str = Field(pattern=password_regex, min_length=8)


class UserUpdate(BaseModel):
    """Request body input as a class for updating a user's details."""

    email: str | None = Field(default=None, pattern=email_regex)
    password: str | None = Field(default=None, pattern=password_regex, min_length=8)


class UserResponse(BaseModel):
    """Used when returning to the user (removes sensitive info like passwords)."""

    id: int = Field(ge=1)
    email: str = Field(pattern=email_regex)

    class Config:
        """Config subclass of UserResponse."""

        from_attributes: bool = True
