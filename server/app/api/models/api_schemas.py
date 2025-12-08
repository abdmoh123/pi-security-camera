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


class UserResponse(BaseModel):
    """Used when returning to the user (removes sensitive info like passwords)."""

    id: int
    email: str

    class Config:
        """Config subclass of UserResponse."""

        from_attributes: bool = True


class Camera(BaseModel):
    """Pydantic model for a camera."""

    id: int
    host_address: str
    name: str
    auth_key: str
    mac_address: str

    class Config:
        """Config subclass of Camera."""

        from_attributes: bool = True


class CameraCreate(BaseModel):
    """Pydantic model received when creating a new camera record."""

    host_address: str
    name: str
    auth_key: str
    mac_address: str


class CameraUpdate(BaseModel):
    """Pydantic model used when updating a Camera record."""

    name: str | None = None
    host_address: str | None = None
    auth_key: str | None = None
    mac_address: str | None = None


class CameraSubscription(BaseModel):
    """Pydantic model for a subscription of a user to a camera."""

    user_id: int
    camera_id: int

    class Config:
        """Config subclass of CameraSubscription."""

        from_attributes: bool = True


class Video(BaseModel):
    """Pydantic model for a video entry."""

    id: int
    file_name: str
    camera_id: int

    class Config:
        """Config subclass of Video."""

        from_attributes: bool = True


class VideoCreate(BaseModel):
    """Pydantic model for a video entry."""

    file_name: str
    camera_id: int


class VideoUpdate(BaseModel):
    """Pydantic model for modifying the video entry in the database."""

    file_name: str | None = None
