"""File containing pydantic models for camera subscription data."""

from pydantic import BaseModel, Field


class CameraSubscription(BaseModel):
    """Pydantic model for a subscription of a user to a camera."""

    user_id: int = Field(ge=1)
    camera_id: int = Field(ge=1)

    class Config:
        """Config subclass of CameraSubscription."""

        from_attributes: bool = True
