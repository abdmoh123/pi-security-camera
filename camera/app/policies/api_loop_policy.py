"""Main SurveillanceSystem loop with video uploads to a remote server."""

from dataclasses import dataclass

from app.fsms.camera.types import CameraState
from app.services.api.api_service import APIService
from app.surveillance_system import SurveillanceSystem


@dataclass(frozen=True)
class APILoopPolicy:
    """Main SurveillanceSystem loop with video uploads to a remote server.

    Attributes:
        camera_system: The camera state machine wrapper.
        api_service: The API service.
    """

    camera_system: SurveillanceSystem
    api_service: APIService

    def run_loop(self) -> None:
        """Main loop for the surveillance system system."""
        # Generator has an infinite loop
        for event in self.camera_system.events():
            # Exit the loop if the camera is stopped.
            if self.camera_system.state is CameraState.STOPPED:
                break
            self.camera_system.handle_event(event)

            # Upload the video if the API server is reachable
            if self.camera_system.state is CameraState.SAVING:
                try:
                    self.api_service.upload_video(
                        self.camera_system.context.file_manager.get_latest_file()
                    )
                except Exception as e:
                    print(e)
