"""Tests for the camera service."""

import re
from pathlib import Path

import numpy as np
from cv2.typing import MatLike
from pytest_mock import MockFixture

from app.core.cameras.camera import Camera
from app.core.serializers.serializer import Serializer
from app.services.camera_service import CameraService


def test_camera_service_record_video(mocker: MockFixture) -> None:
    """Test the camera service."""
    # Create fake video data (3 colours BGR at 640x480 resolution)
    fake_data: list[MatLike] = [
        np.zeros((480, 640, 3), dtype=np.uint8),  # Black
        np.full((480, 640, 3), 128, dtype=np.uint8),  # Grey
        np.full((480, 640, 3), 255, dtype=np.uint8),  # White
    ]

    mocked_camera = mocker.MagicMock(spec=Camera)
    mock_start_recording = mocker.patch.object(
        mocked_camera, "start_recording", return_value=fake_data
    )

    mocked_serializer = mocker.MagicMock(spec=Serializer)
    mock_write_video = mocker.patch.object(mocked_serializer, "write_video")

    # Disable the Path mkdir method to prevent creating directories
    _ = mocker.patch.object(Path, "mkdir")

    camera_service = CameraService(mocked_camera, mocked_serializer)

    # Call the method
    camera_service.record_video(0)

    # Check if the start_recording method was called
    mock_start_recording.assert_called_once_with(0)

    # Check if writing the file was attempted
    mock_write_video.assert_called_once()

    # Check if the data being written matches the mocked camera data
    actual_data: list[MatLike]
    actual_file_path: Path
    actual_data, actual_file_path = mock_write_video.call_args.args  # pyright: ignore[reportAny]
    np.testing.assert_array_equal(actual_data, fake_data)

    # Check if the file path is correct
    assert actual_file_path.parent == Path("./recordings")
    assert re.match(
        r"video-\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.mp4",
        actual_file_path.name,
    )
    assert actual_file_path.suffix == ".mp4"
