"""Model for a camera's data."""

from pydantic import BaseModel, Field

# As long as the name starts with a letter (case-insensitive)
camera_name_regex: str = r"^[a-zA-Z]+.*$"
# Regex pattern for the ipv4 format
host_address_regex: str = r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$"
# Regex pattern for the MAC address format
mac_address_regex: str = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"


class BaseCamera(BaseModel):
    """Base model for a camera's data.

    Attributes:
        name: A camera's name
    """

    name: str = Field(pattern=camera_name_regex)


class CameraCreate(BaseCamera):
    """Pydantic model used when creating a Camera record.

    Attributes:
        name: The camera's name
        mac_address: The camera's MAC address
    """

    mac_address: str = Field(pattern=mac_address_regex)


class Camera(BaseModel):
    """Model for the camera's data gained from the server API.

    Attributes:
        id: A camera's ID
        host_address: A camera's host address
        name: A camera's name
        mac_address: A camera's MAC address
    """

    id: int = Field(ge=1)
    name: str = Field(pattern=camera_name_regex)
    mac_address: str = Field(pattern=mac_address_regex)

    class Config:
        """Config subclass of Camera."""

        from_attributes: bool = True


class CameraUpdate(BaseModel):
    """Pydantic model used when updating a Camera record."""

    name: str | None = Field(default=None, pattern=camera_name_regex)
    auth_key: str | None = None
    mac_address: str | None = Field(default=None, pattern=mac_address_regex)
