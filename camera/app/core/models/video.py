"""Model for video data from the server."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Video:
    """Model for a video entry data gained from the server API.

    Attributes:
        id: A video's ID
        file_name: A video's file name
    """

    id: str
    file_name: str
