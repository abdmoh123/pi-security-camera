"""Model for a camera's data."""

from pydantic import BaseModel, Field

# As long as the name starts with a letter (case-insensitive)
camera_name_regex: str = r"^[a-zA-Z]+.*$"
# Regex pattern for the ipv4 format
host_address_regex: str = r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$"
# Regex pattern for the MAC address format
mac_address_regex: str = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"


class CameraUpdate(BaseModel):
    """Pydantic model used when updating a Camera record."""

    name: str | None = Field(default=None, pattern=camera_name_regex)
    host_address: str | None = Field(default=None, pattern=host_address_regex)
    auth_key: str | None = None
    mac_address: str | None = Field(default=None, pattern=mac_address_regex)
