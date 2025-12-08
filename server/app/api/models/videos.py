"""File containing pydantic models for video data."""

from pydantic import BaseModel


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
