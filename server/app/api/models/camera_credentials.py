"""File containing pydantic models for camera credential data."""

from pydantic import BaseModel


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
