"""File containing pydantic models for user data."""

from pydantic import BaseModel, Field

from app.core.validation.regex import email_regex


class User(BaseModel):
    """Base User record/model."""

    id: int = Field(ge=1)
    email: str = Field(pattern=email_regex)  # Rudimentary validation (won't check if email exists)
    password_hash: str = Field(min_length=8)  # Password rules can't apply here as it is a hash

    class Config:
        """Config subclass of User."""

        from_attributes: bool = True


class UserCreate(BaseModel):
    """Request body input as a class for creating a new user."""

    email: str = Field(pattern=email_regex)
    password_hash: str = Field(min_length=8)


class UserUpdate(BaseModel):
    """Request body input as a class for updating a user's details."""

    email: str | None = Field(default=None, pattern=email_regex)
    password_hash: str | None = Field(default=None, min_length=8)


class UserResponse(BaseModel):
    """Used when returning to the user (removes sensitive info like passwords)."""

    id: int = Field(ge=1)
    email: str = Field(pattern=email_regex)

    class Config:
        """Config subclass of UserResponse."""

        from_attributes: bool = True
