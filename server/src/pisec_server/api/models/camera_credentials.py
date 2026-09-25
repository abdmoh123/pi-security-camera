"""File containing pydantic models for camera credential data."""

from datetime import datetime

from pydantic import BaseModel


class CameraCredentialRedactedResponse(BaseModel):
    """Pydantic model for a camera credential without sensitive data."""

    client_id: str
    user_id: int
    camera_id: int | None = None  # Not null if credential linked to a camera
    registered_at: datetime


class CameraCredentialResponse(BaseModel):
    """Pydantic model for returning camera credential data."""

    client_id: str  # Kind of like a UUID
    user_id: int
    client_secret: str  # Required as it is randomly generated


class CameraCredentialCreate(BaseModel):
    """Pydantic model for creating new camera credential data."""

    client_id: str  # Kind of like a UUID
    client_secret: str

    class Config:
        """Config subclass for CameraCredential."""

        from_attributes: bool = True
