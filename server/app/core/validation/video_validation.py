"""A set of validation functions related to videos."""

from pathlib import Path

from app.core.config import settings
from app.core.exceptions import InvalidFileNameError


def get_video_file_path_safe(file_name: str, camera_id: int) -> Path:
    """Validates the video file name."""
    # Path is resolved to get rid of '..'s, '.'s and symlinks
    file_path: Path = (settings.VIDEO_FILES_DIR / str(camera_id) / file_name).resolve()

    # Reduce chance of injecting file paths to gain access to arbitrary files
    # Technically this is overkill because a regex check is done at the pydantic
    # model level, making it impossible to inject a file path
    if file_path.parent.name != str(camera_id) or file_path.parent.parent != settings.VIDEO_FILES_DIR:
        raise InvalidFileNameError("Invalid file name!")

    return file_path
