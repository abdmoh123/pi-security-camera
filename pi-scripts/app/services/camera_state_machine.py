"""A state machine implementation for the motion detection system."""

import time
from collections.abc import Generator
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import ClassVar

from cv2.typing import MatLike

from app.core.cameras.camera import Camera
from app.core.serializers.serializer import Serializer
from app.core.state_machine import SMContext, StateMachine
from app.services.file_manager import FileManager
from app.services.file_name_generator import generate_timestamp_video_name
from app.services.motion.motion_detector import MotionDetectorService


class CameraState(StrEnum):
    """The states of the camera."""
    DETECTING = auto()
    RECORDING = auto()
    SAVING = auto()
    SLEEPING = auto()
    STOPPED = auto()


class CameraEvent(StrEnum):
    """The events of the camera."""
    RECORD = auto()
    SAVE = auto()
    SLEEP = auto()
    STOP = auto()


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


__camera_fsm: StateMachine[CameraState, CameraEvent, CameraCtx] = StateMachine(
    CameraEvent.STOP
)


def __motion_detect_guard(context: CameraCtx) -> bool:
    return context.motion_detector.detect_motion(
        context.settings.detect_delta_ms
    )


@__camera_fsm.transition(
    CameraState.DETECTING,
    CameraState.RECORDING,
    CameraEvent.RECORD,
    __motion_detect_guard
)
def __record_action(context: CameraCtx) -> None:  # pyright: ignore[reportUnusedFunction]
    context.data = context.camera.start_recording(
        context.settings.video_length_s
    )


@__camera_fsm.transition(
    CameraState.DETECTING,
    CameraState.DETECTING,
    CameraEvent.RECORD,
)
def __skip_record_action(_: CameraCtx) -> None:  # pyright: ignore[reportUnusedFunction]
    print("Motion not detected, skipping recording...")


@__camera_fsm.transition(
    CameraState.RECORDING,
    CameraState.SAVING,
    CameraEvent.SAVE
)
def __save_action(context: CameraCtx) -> None:  # pyright: ignore[reportUnusedFunction]
    if not context.data:
        raise ValueError("No data to save")

    context.file_manager.save_data(
        context.data, generate_timestamp_video_name, context.serializer
    )
    context.data = None


@__camera_fsm.transition(
    (CameraState.DETECTING, CameraState.SAVING),
    CameraState.SLEEPING,
    CameraEvent.SLEEP
)
def __sleep_action(context: CameraCtx) -> None:  # pyright: ignore[reportUnusedFunction]
    print(
        f"Sleeping for {context.settings.wait_time_ms // 1000} seconds..."
    )
    time.sleep(context.settings.wait_time_ms // 1000)


@__camera_fsm.transition(
    (
        CameraState.DETECTING,
        CameraState.RECORDING,
        CameraState.SAVING,
        CameraState.SLEEPING
    ),
    CameraState.STOPPED,
    CameraEvent.STOP
)
def __shutdown(context: CameraCtx) -> None:  # pyright: ignore[reportUnusedFunction]
    if context.error:
        print(f"Error has occured: {context.error}")
    print("Shutting down...")
    context.camera.disable()


@dataclass
class CameraFSM:
    """A camera system using the state machine pattern.

    Attributes:
        context: The context/data of the camera system.
        state: The current state of the camera system. Defaults to DETECTING.
    """

    context: CameraCtx
    state: CameraState = CameraState.DETECTING

    _event_loop: ClassVar[tuple[CameraEvent, ...]] = (
        CameraEvent.RECORD, CameraEvent.SAVE, CameraEvent.SLEEP
    )
    # Don't run the save event if the camera is in the detect state
    # As no data has been recorded
    _skip_transitions: ClassVar[list[tuple[CameraState, CameraEvent]]] = [
        (CameraState.DETECTING, CameraEvent.SAVE)
    ]

    def events(self) -> Generator[CameraEvent, None, None]:
        """Iterates through the event loop of the camera system."""
        while True:
            for event in CameraFSM._event_loop:
                if (self.state, event) in CameraFSM._skip_transitions:
                    continue
                yield event

    def handle_event(self, event: CameraEvent) -> None:
        """Handles an event and updates the camera system state.

        Args:
            event: The event to handle.
        """
        self.state = __camera_fsm.handle_event(self.state, event, self.context)
