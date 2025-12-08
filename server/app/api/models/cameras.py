"""File containing pydantic models for camera data."""

from pydantic import BaseModel


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
