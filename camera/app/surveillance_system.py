"""A state machine implementation for the motion detection system."""

from collections.abc import Generator
from dataclasses import dataclass
from typing import ClassVar

from app.fsms.camera.camera import camera_fsm
from app.fsms.camera.data import CameraCtx
from app.fsms.camera.types import CameraEvent, CameraState
from app.services.api.api_service import APIService
from app.services.file_manager import FileManager


@dataclass
class SurveillanceSystem:
    """A camera surveillance system using the state machine pattern.

    Attributes:
        context: The context/data of the camera system.
        state: The current state of the camera system. Defaults to DETECTING.
    """

    context: CameraCtx
    state: CameraState = CameraState.DETECTING

    _event_loop: ClassVar[tuple[CameraEvent, ...]] = (
        CameraEvent.RECORD,
        CameraEvent.SAVE,
        CameraEvent.SLEEP,
        CameraEvent.WAKE,
    )
    # Don't run the save event if the camera is in the detect state
    # As no data has been recorded
    _skip_transitions: ClassVar[list[tuple[CameraState, CameraEvent]]] = [
        (CameraState.DETECTING, CameraEvent.SAVE)
    ]

    def events(self) -> Generator[CameraEvent, None, None]:
        """Iterates through the event loop of the camera system."""
        while True:
            for event in SurveillanceSystem._event_loop:
                if (self.state, event) in SurveillanceSystem._skip_transitions:
                    continue
                yield event

    def handle_event(self, event: CameraEvent) -> None:
        """Handles an event and updates the camera system state.

        Args:
            event: The event to handle.
        """
        self.state = camera_fsm.handle_event(self.state, event, self.context)


def run_loop(
    camera_fsm: SurveillanceSystem,
    file_manager: FileManager,
    api_service: APIService | None = None,
) -> None:
    """Main loop for the surveillance system system.

    Args:
        camera_fsm: The camera state machine.
        file_manager: The file manager service.
        api_service: The API service.
    """
    # Generator has an infinite loop
    for event in camera_fsm.events():
        # Exit the loop if the camera is stopped.
        if camera_fsm.state is CameraState.STOPPED:
            break
        camera_fsm.handle_event(event)

        # Upload the video if the API server is reachable
        if api_service is not None and camera_fsm.state is CameraState.SAVING:
            try:
                api_service.upload_video(file_manager.get_latest_file())
            except Exception as e:
                print(e)
