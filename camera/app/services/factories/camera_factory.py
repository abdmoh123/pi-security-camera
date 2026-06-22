"""Factory for choosing between camera types."""

from enum import StrEnum, auto

from app.core.cameras.camera import Camera
from app.core.cameras.dummy_camera import DummyCamera
from app.core.cameras.opencv_camera import OpenCVCamera


class CameraType(StrEnum):
    """Camera types."""

    OPENCV = auto()
    DUMMY = auto()


def create_camera(camera_type: CameraType) -> Camera:
    """Creates a camera of the given type.

    Args:
        camera_type: The type of camera to create.

    Returns:
        A new camera object of the given type.
    """
    match camera_type:
        case CameraType.OPENCV:
            return OpenCVCamera()
        case CameraType.DUMMY:
            return DummyCamera()
