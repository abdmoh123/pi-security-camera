"""Main SurveillanceSystem loop with no API connection."""

from dataclasses import dataclass

from app.fsms.camera.types import CameraState
from app.surveillance_system import SurveillanceSystem


@dataclass(frozen=True)
class OfflineLoopPolicy:
    """Main SurveillanceSystem loop with video uploads to a remote server.

    Attributes:
        camera_system: The camera state machine wrapper.
    """

    camera_system: SurveillanceSystem

    def run_loop(self) -> None:
        """Main loop for the surveillance system system."""
        # Generator has an infinite loop
        for event in self.camera_system.events():
            # Exit the loop if the camera is stopped.
            if self.camera_system.state is CameraState.STOPPED:
                break
            self.camera_system.handle_event(event)
