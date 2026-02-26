from typing import Annotated
from fastapi import APIRouter, Query

import app.services.camera as camera_service

router = APIRouter(prefix="/run", tags=["runner"])


@router.post("/record")
def start_recording(time_s: Annotated[int, Query()]) -> None:
    """Starts the camera recording routine."""
    camera_service.start_recording(time_s)


@router.post("/disable")
def disable_motion_detection(time_s: Annotated[int, Query()]) -> None:
    """Disables the camera's motion detection recording routine."""
    camera_service.disable_motion_detection(time_s)


@router.post("/enable")
def enable_motion_detection(time_s: Annotated[int, Query()]) -> None:
    """Enables the camera's motion detection recording routine."""
    camera_service.enable_motion_detection(time_s)
