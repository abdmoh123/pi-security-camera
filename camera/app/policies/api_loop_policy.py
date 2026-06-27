"""Main SurveillanceSystem loop with video uploads to a remote server."""

from dataclasses import dataclass
from typing import override

from app.fsms.camera.types import CameraState
from app.policies.loop_policy import AbstractLoopPolicy
from app.services.api.api_service import APIService
from app.services.api.auth import OAuth2Authenticator


@dataclass(frozen=True)
class APILoopPolicy(AbstractLoopPolicy):
    """Main SurveillanceSystem loop with video uploads to a remote server.

    Attributes:
        camera_system: The camera state machine wrapper.
        api_service: The API service.
    """

    api_url: str
    authenticator: OAuth2Authenticator

    @override
    def run_loop(self) -> None:
        """Main loop for the surveillance system system."""
        with APIService(self.api_url, self.authenticator) as api_service:
            # Generator has an infinite loop
            for event in self.camera_system.events():
                # Exit the loop if the camera is stopped.
                if self.camera_system.state is CameraState.STOPPED:
                    break
                self.camera_system.handle_event(event)

                # Upload the video if the API server is reachable
                if self.camera_system.state is CameraState.SAVING:
                    try:
                        api_service.upload_video(
                            self.camera_system.context.file_manager.get_latest_file()
                        )
                    except Exception as e:
                        print(e)
