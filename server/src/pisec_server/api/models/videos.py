"""File containing pydantic models for video data."""

from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field

from pisec_server.core.validation.regex import file_name_regex


class Video(BaseModel):
    """Pydantic model for a video entry."""

    id: int = Field(ge=1)
    file_name: str = Field(pattern=file_name_regex, min_length=5)
    camera_id: int = Field(ge=1)
    uploaded_at: datetime

    class Config:
        """Config subclass of Video."""

        from_attributes: bool = True


class VideoResponse(Video):
    """Alias for Video to match other model types pattern."""


class VideoCreate(BaseModel):
    """Pydantic model for a video entry."""

    file_name: str = Field(pattern=file_name_regex, min_length=5)


class VideoUpdate(BaseModel):
    """Pydantic model for modifying the video entry in the database."""

    file_name: str | None = Field(default=None, pattern=file_name_regex, min_length=5)


class VideoUrlResponse(BaseModel):
    """Pydantic model for video url token."""

    url: str
    expires_at: datetime


class VideoFileData(BaseModel):
    """Model for data required for FileResponse."""

    file_path: Path
    file_name: str
    media_type: str
