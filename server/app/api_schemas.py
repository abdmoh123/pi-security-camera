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


class Camera(BaseModel):
    """Pydantic model for a camera."""

    id: int
    name: str
    auth_key: str
    mac_address: str

    class Config:
        """Config subclass of Camera."""

        from_attributes: bool = True


class CameraCreate(BaseModel):
    """Pydantic model used when creating a new camera record."""

    name: str
    auth_key: str
    mac_address: str


class CameraUpdate(BaseModel):
    """Pydantic model used when updating a Camera record."""

    name: str | None = None
    auth_key: str | None = None
    mac_address: str | None = None
