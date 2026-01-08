"""FastAPI routes related to the Camera table."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.api.models.cameras import CameraCreate, CameraResponse, CameraUpdate
from app.api.models.general import PaginationParams
from app.api.models.videos import Video
from app.auth.dependencies import get_current_admin_user, get_current_user
from app.core.validation.regex import camera_name_regex, host_address_regex, mac_address_regex
from app.db.database import get_db
from app.db.db_models import Camera as CameraSchema
from app.db.db_models import User as UserSchema
from app.db.db_models import Video as VideoSchema
from app.services import camera as camera_service
from app.services import video as video_service

router = APIRouter(prefix="/cameras", tags=["cameras"])


@router.get("/", response_model=list[CameraResponse])
def get_cameras(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    pagination: Annotated[PaginationParams, Query()],
    db_session: Annotated[Session, Depends(get_db)],
    id: Annotated[list[int] | None, Query(ge=1)] = None,
    name: Annotated[str | None, Query(regex=camera_name_regex)] = None,
    host_address: Annotated[str | None, Query(regex=host_address_regex)] = None,
    mac_address: Annotated[str | None, Query(regex=mac_address_regex)] = None,
) -> list[CameraSchema]:
    """Gets a list of all cameras with pagination.

    Non-admin users can only see cameras they are subscribed to.
    """
    cameras = camera_service.get_cameras(
        db_session,
        id,
        name,
        host_address,
        mac_address,
        pagination.page_index * pagination.page_size,
        pagination.page_size,
    )

    if not current_user.is_admin:
        # Filter to only show cameras the user is subscribed to
        subscribed_camera_ids = {camera.id for camera in current_user.cameras}
        cameras = [camera for camera in cameras if camera.id in subscribed_camera_ids]

    return cameras


@router.post("/", response_model=CameraResponse)
def create_camera(
    current_user: Annotated[UserSchema, Depends(get_current_user)],  # pyright: ignore[reportUnusedParameter]
    camera: Annotated[CameraCreate, Body()],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSchema:
    """Creates a new camera with given details."""
    db_cameras: list[CameraSchema] = camera_service.get_cameras(db_session, host_address=camera.host_address, limit=1)

    if db_cameras:
        raise HTTPException(status_code=400, detail="Camera already exists: Host address is already in use!")

    return camera_service.create_camera(db_session, camera)


@router.get("/{id}", response_model=CameraResponse)
def get_camera(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    id: Annotated[int, Path(ge=1)],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSchema:
    """Returns a camera's details using a given ID."""
    db_camera: CameraSchema | None = camera_service.get_camera(db_session, id)

    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found!")

    # Only allow access if user is subscribed to the camera or is an admin
    if not current_user.is_admin and db_camera not in current_user.cameras:
        raise HTTPException(status_code=403, detail="Not subscribed to this camera")

    return db_camera


@router.put("/{id}", response_model=CameraResponse)
def update_camera(
    current_user: Annotated[UserSchema, Depends(get_current_admin_user)],
    id: Annotated[int, Path(ge=1)],
    camera: Annotated[CameraUpdate, Body()],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSchema:
    """Updates a camera's details using a given ID. Admin only."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if camera.host_address:
        cameras_by_ip: list[CameraSchema] = camera_service.get_cameras(
            db_session, host_address=camera.host_address, limit=1
        )
        if cameras_by_ip and cameras_by_ip[0].id != id:
            raise HTTPException(status_code=409, detail="Failed to change Host address: Already in use!")

    db_camera: CameraSchema | None = camera_service.update_camera(db_session, id, camera)
    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found!")

    return db_camera


@router.delete("/{id}", response_model=CameraResponse)
def delete_camera(
    current_user: Annotated[UserSchema, Depends(get_current_admin_user)],
    id: Annotated[int, Path(ge=1)],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSchema:
    """Deletes a given camera by ID. Admin only."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_camera: CameraSchema | None = camera_service.delete_camera(db_session, camera_id=id)
    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    return db_camera


@router.get("/{id}/videos", response_model=list[Video])
def get_videos(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    id: Annotated[int, Path(ge=1)],
    pagination: Annotated[PaginationParams, Query()],
    db_session: Annotated[Session, Depends(get_db)],
) -> list[VideoSchema]:
    """Gets a list of all of a camera's videos with pagination."""
    db_camera: CameraSchema | None = camera_service.get_camera(db_session, id)
    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found!")

    # Only allow access if user is subscribed to the camera or is an admin
    if not current_user.is_admin and db_camera not in current_user.cameras:
        raise HTTPException(status_code=403, detail="Not subscribed to this camera")

    return video_service.get_video_entries(
        db_session,
        camera_ids=[db_camera.id],
        skip=pagination.page_index * pagination.page_size,
        limit=pagination.page_size,
    )
