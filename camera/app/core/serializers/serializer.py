"""Generic Protocol for serialization."""

from pathlib import Path
from typing import Protocol

from cv2.typing import MatLike


class Serializer(Protocol):
    """Generic Protocol for serialization."""

    def write_video(self, data: list[MatLike], file_path: Path) -> None:
        """Writes video data to a file.

        Args:
            data: The video data to write.
            file_path: The path to write the video to.
        """
        ...

    def write_image(self, data: MatLike, file_path: Path) -> None:
        """Writes image data to a file.

        Args:
            data: The image data to write.
            file_path: The path to write the image to.
        """
        ...
