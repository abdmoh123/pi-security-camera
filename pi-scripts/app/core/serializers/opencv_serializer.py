"""OpenCV based implementation of the Serializer protocol."""

from pathlib import Path

import cv2
from cv2 import (  # type: ignore[attr-defined]
    VideoWriter,
    VideoWriter_fourcc,  # pyright: ignore[reportAttributeAccessIssue, reportUnknownVariableType]
)
from cv2.typing import MatLike

from app.core.exceptions.serialization import SerializationError


class OpenCVSerializer:
    """OpenCV based implementation of the Serializer protocol."""

    def write_video(self, data: list[MatLike], file_path: Path) -> None:
        """OpenCV based implementation of the write_video method."""
        out = VideoWriter(
            filename=file_path,
            fourcc=VideoWriter_fourcc(*"mp4v"),  # pyright: ignore[reportUnknownArgumentType]
            fps=24.0,
            frameSize=data[0].shape[1::-1],  # pyright: ignore[reportAny]
        )
        for frame in data:
            out.write(frame)
        out.release()

    def write_image(self, data: MatLike, file_path: Path) -> None:
        """OpenCV based implementation of the write_image method."""
        res: bool = cv2.imwrite(file_path, data)
        if not res:
            raise SerializationError(file_path)
