"""Tests for the camera service."""

import re
from pathlib import Path
from typing import Callable

import numpy as np
from cv2.typing import MatLike
from pytest_mock import MockFixture

from app.core.cameras.camera import Camera
from app.core.serializers.serializer import Serializer
from app.services.camera_service import CameraService
from app.services.file_manager import FileManager


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

    mocked_file_manager = mocker.MagicMock(spec=FileManager)
    mock_save_data = mocker.patch.object(mocked_file_manager, "save_data")

    # Disable the Path mkdir method to prevent creating directories
    _ = mocker.patch.object(Path, "mkdir")

    camera_service = CameraService(
        mocked_camera, mocked_serializer, mocked_file_manager
    )

    # Call the method
    camera_service.record_video(0)

    # Check if the start_recording method was called
    mock_start_recording.assert_called_once_with(0)

    # Check if writing the file was attempted
    mock_save_data.assert_called_once()

    # Read passed arguments to the mocked file manager
    actual_data: list[MatLike]
    file_name_generator: Callable[[], str]
    passed_serializer: Serializer
    actual_data, file_name_generator, passed_serializer = (  # pyright: ignore[reportAny]
        mock_save_data.call_args.args
    )

    # Check if the data being written matches the mocked camera data
    np.testing.assert_array_equal(actual_data, fake_data)

    # File manager should use the same serializer passed to the camera service
    assert passed_serializer == mocked_serializer

    # Check if the file path generator is correct
    generated_file_name: str = file_name_generator()
    assert re.match(
        r"video-\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.mp4",
        generated_file_name,
    )
    assert generated_file_name.split(".")[-1] == "mp4"
