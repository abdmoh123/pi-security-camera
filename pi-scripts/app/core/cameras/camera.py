"""Protocol for camera implementations."""

from typing import Protocol

from cv2.typing import MatLike


class Camera(Protocol):
    """Generic camera protocol."""

    def capture_frame(self) -> MatLike:
        """Captures the current frame from the camera."""
        ...

    def start_recording(self, time_s: int = 600) -> list[MatLike]:
        """Starts the camera recording routine."""
        ...
