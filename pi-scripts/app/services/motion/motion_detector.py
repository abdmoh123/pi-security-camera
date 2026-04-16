"""Service for detecting motion in the camera feed."""

from typing import Protocol


class MotionDetectorService(Protocol):
    """Protocol for motion detection services."""

    def detect_motion(self, delta_ms: int = 1000) -> bool:
        """Detects motion in the camera feed.

        Returns:
            True if motion is detected, False otherwise.
        """
        ...
