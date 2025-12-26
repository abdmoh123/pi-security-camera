"""File containing pydantic models for video data."""

from pydantic import BaseModel, Field


class Video(BaseModel):
    """Pydantic model for a video entry."""

    id: int = Field(ge=1)
    file_name: str = Field(min_length=5)
    camera_id: int = Field(ge=1)

    class Config:
        """Config subclass of Video."""

        from_attributes: bool = True


class VideoCreate(BaseModel):
    """Pydantic model for a video entry."""

    file_name: str = Field(min_length=5)
    camera_id: int = Field(ge=1)


class VideoUpdate(BaseModel):
    """Pydantic model for modifying the video entry in the database."""

    file_name: str | None = Field(default=None, min_length=5)
