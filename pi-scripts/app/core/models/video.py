"""Model for video data from the server."""

from dataclasses import dataclass


@dataclass
class Video:
    """Model for a user's data."""

    id: str
    file_name: str
