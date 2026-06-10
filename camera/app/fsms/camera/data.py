"""Data structures used by the camera state machine."""

from dataclasses import dataclass

from cv2.typing import MatLike

from app.core.cameras.camera import Camera
from app.core.serializers.serializer import Serializer
from app.core.state_machine import SMContext
from app.services.file_manager import FileManager
from app.services.motion.motion_detector import MotionDetectorService


@dataclass(frozen=True)
class CameraSettings:
    """Settings for the camera."""

    wait_time_ms: int = 1000
    detect_delta_ms: int = 500
    video_length_s: int = 10


@dataclass
class CameraCtx(SMContext):
    """Data to be used by the camera state machine."""

    camera: Camera
    motion_detector: MotionDetectorService
    file_manager: FileManager
    serializer: Serializer

    settings: CameraSettings

    data: list[MatLike] | None = None
