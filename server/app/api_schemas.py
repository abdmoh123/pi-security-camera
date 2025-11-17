"""File containing Pydantic models used to verify inputted REST API request bodies."""

from pydantic import BaseModel


class User(BaseModel):
    """Base User record/model."""

    id: int
    email: str
    password_hash: str

    class Config:
        """Config subclass of User."""

        from_attributes: bool = True


class UserCreate(BaseModel):
    """Request body input as a class for creating a new user."""

    email: str
    password_hash: str


class UserUpdate(BaseModel):
    """Request body input as a class for updating a user's details."""

    email: str | None = None
    password_hash: str | None = None
