"""Model for video data from the server."""

from pydantic import BaseModel, Field

# Any name excluding '/' characters
file_name_regex: str = r"video-\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.mp4"


class Video(BaseModel):
    """Model for a video entry data gained from the server API.

    Attributes:
        id: A video's ID
        file_name: A video's file name
    """

    id: int = Field(ge=1)
    file_name: str = Field(pattern=file_name_regex, min_length=5)
    camera_id: int = Field(ge=1)

    class Config:
        """Config subclass of Video."""

        from_attributes: bool = True
