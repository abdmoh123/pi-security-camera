"""Generic camera implementation using opencv."""

import time
from types import TracebackType
from typing import Self

import cv2
from cv2.typing import MatLike


class OpenCVCamera:
    """Generic camera implementation using opencv."""

    def __init__(self, camera_id: int = 0) -> None:
        """Initializes the camera."""
        self.camera: cv2.VideoCapture = cv2.VideoCapture(camera_id)

    def __enter__(self) -> Self:
        """Method for use with the 'with' statement."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Releases the camera."""
        self.camera.release()

    def capture_frame(self) -> MatLike:
        """Captures the current frame from the camera."""
        ret, frame = self.camera.read()
        if not ret:
            raise RuntimeError("Failed to capture frame")
        return frame

    def start_recording(self, time_s: int = 600) -> list[MatLike]:
        """Starts the camera recording routine."""
        frame_rate: int = 24  # fps

        frames: list[MatLike] = []
        frames_to_capture = int(time_s * frame_rate)
        for _ in range(frames_to_capture):
            ret, frame = self.camera.read()

            # If the frame couldn't be captured, break early
            if not ret:
                break

            frames.append(frame)
            time.sleep(1.0 / frame_rate)

        return frames
