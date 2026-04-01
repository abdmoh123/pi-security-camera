"""Tests for the video validation module."""

import pytest

from app.core.config import settings
from app.core.exceptions import InvalidFileNameError
from app.core.validation.video_validation import get_video_file_path_safe


def test_get_video_file_path_safe_valid() -> None:
    """Test the safe video file path generator function with valid inputs."""
    assert (
        get_video_file_path_safe("video-2026-01-11_14-38-32.mp4", 1)
        == settings.VIDEO_FILES_DIR / "1" / "video-2026-01-11_14-38-32.mp4"
    )
    assert (
        get_video_file_path_safe("video-2026-01-11_14-38-32.mp4", 5)
        == settings.VIDEO_FILES_DIR / "5" / "video-2026-01-11_14-38-32.mp4"
    )


def test_get_video_file_path_safe_injection() -> None:
    """Test the safe video file path generator function with invalid injection inputs."""
    # Attempt to copy the video to someone else's camera
    with pytest.raises(InvalidFileNameError):
        _ = get_video_file_path_safe("../10/test.mp4", 1)
    # Attempt to replace the cd command with an uploaded file
    with pytest.raises(InvalidFileNameError):
        _ = get_video_file_path_safe("~/../../usr/bin/cd", 0)


def test_get_video_file_path_safe_invalid() -> None:
    """Test the safe video file path generator function with inputs with unconventional symbols."""
    with pytest.raises(InvalidFileNameError):
        _ = get_video_file_path_safe("test.mp4", 1)
    with pytest.raises(InvalidFileNameError):
        _ = get_video_file_path_safe("$!A.fdguhs2p4.", 2)
    with pytest.raises(InvalidFileNameError):
        _ = get_video_file_path_safe("\n3()f{`'print(1)}.p4", 3)
