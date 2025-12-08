"""File containing pydantic models for camera subscription data."""

from pydantic import BaseModel


class CameraSubscription(BaseModel):
    """Pydantic model for a subscription of a user to a camera."""

    user_id: int
    camera_id: int

    class Config:
        """Config subclass of CameraSubscription."""

        from_attributes: bool = True
