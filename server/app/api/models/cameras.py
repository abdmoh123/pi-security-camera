"""File containing pydantic models for camera data."""

from pydantic import BaseModel, Field

from app.core.validation.regex import camera_name_regex, host_address_regex, mac_address_regex


class CameraResponse(BaseModel):
    """Pydantic model returned to the client.

    Similar to Camera but it doesn't contain sensitive fields like auth_key.
    """

    id: int = Field(ge=1)
    host_address: str = Field(pattern=host_address_regex)
    name: str = Field(pattern=camera_name_regex)
    mac_address: str = Field(pattern=mac_address_regex)

    class Config:
        """Config subclass of CameraResponse."""

        from_attributes: bool = True


class Camera(BaseModel):
    """Pydantic model for a camera."""

    id: int = Field(ge=1)
    host_address: str = Field(pattern=host_address_regex)
    name: str = Field(pattern=camera_name_regex)
    auth_key: str
    mac_address: str = Field(pattern=mac_address_regex)

    class Config:
        """Config subclass of Camera."""

        from_attributes: bool = True


class CameraCreate(BaseModel):
    """Pydantic model received when creating a new camera record."""

    host_address: str = Field(pattern=host_address_regex)
    name: str = Field(pattern=camera_name_regex)
    auth_key: str
    mac_address: str = Field(pattern=mac_address_regex)


class CameraUpdate(BaseModel):
    """Pydantic model used when updating a Camera record."""

    name: str | None = Field(default=None, pattern=camera_name_regex)
    host_address: str | None = Field(default=None, pattern=host_address_regex)
    auth_key: str | None = None
    mac_address: str | None = Field(default=None, pattern=mac_address_regex)
