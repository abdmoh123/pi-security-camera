"""Factory for choosing between camera types."""

from pisec_cam.core.cameras.camera import Camera
from pisec_cam.core.cameras.dummy_camera import DummyCamera
from pisec_cam.core.cameras.opencv_camera import OpenCVCamera
from pisec_cam.core.types.camera_type import CameraType


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
