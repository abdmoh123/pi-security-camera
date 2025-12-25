"""FastAPI routes related to the Camera table."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.api.models.cameras import Camera, CameraCreate, CameraUpdate
from app.api.models.general import PaginationParams
from app.api.models.videos import Video
from app.core.validation.regex import camera_name_regex, host_address_regex, mac_address_regex
from app.crud import camera as crud_camera
from app.crud import video as crud_video
from app.db.database import get_db
from app.db.db_models import Camera as CameraSchema
from app.db.db_models import Video as VideoSchema

router = APIRouter(prefix="/cameras", tags=["cameras"])


@router.get("/", response_model=list[Camera])
def get_cameras(
    pagination: Annotated[PaginationParams, Query()],
    db_session: Annotated[Session, Depends(get_db)],
    id: Annotated[list[int] | None, Query(ge=1)] = None,
    name: Annotated[str | None, Query(regex=camera_name_regex)] = None,
    host_address: Annotated[str | None, Query(regex=host_address_regex)] = None,
    mac_address: Annotated[str | None, Query(regex=mac_address_regex)] = None,
) -> list[CameraSchema]:
    """Gets a list of all cameras with pagination."""
    return crud_camera.get_cameras(
        db_session,
        id,
        name,
        host_address,
        mac_address,
        pagination.page_index * pagination.page_size,
        pagination.page_size,
    )


@router.post("/", response_model=Camera)
def create_camera(
    camera: Annotated[CameraCreate, Body()],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSchema:
    """Creates a new camera with the given details."""
    db_cameras: list[CameraSchema] = crud_camera.get_cameras(db_session, host_address=camera.host_address, limit=1)

    if db_cameras:
        raise HTTPException(status_code=400, detail="Camera already exists: Host address is already in use!")

    return crud_camera.create_camera(db_session, camera)


@router.get("/{camera_id}", response_model=Camera)
def get_camera(
    id: Annotated[int, Path(ge=1)],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSchema:
    """Returns a camera's details using a given ID."""
    db_camera: CameraSchema | None = crud_camera.get_camera(db_session, id)

    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found!")

    return db_camera


@router.put("/{camera_id}", response_model=Camera)
def update_camera(
    id: Annotated[int, Path(ge=1)],
    camera: Annotated[CameraUpdate, Body()],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSchema:
    """Updates a camera's details using a given ID."""
    if camera.host_address:
        cameras_by_ip: list[CameraSchema] = crud_camera.get_cameras(
            db_session, host_address=camera.host_address, limit=1
        )
        if cameras_by_ip and cameras_by_ip[0].id != id:
            raise HTTPException(status_code=409, detail="Failed to change Host address: Already in use!")

    db_camera: CameraSchema | None = crud_camera.update_camera(db_session, id, camera)

    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found!")

    return db_camera


@router.delete("/{camera_id}", response_model=Camera)
def delete_camera(
    id: Annotated[int, Path(ge=1)],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSchema:
    """Deletes a given camera by ID."""
    db_camera: CameraSchema | None = crud_camera.delete_camera(db_session, camera_id=id)

    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    return db_camera


@router.get("/{camera_id}/videos", response_model=list[Video])
def get_videos(
    id: Annotated[int, Path(ge=1)],
    pagination: Annotated[PaginationParams, Query()],
    db_session: Annotated[Session, Depends(get_db)],
) -> list[VideoSchema]:
    """Gets a list of all of a camera's videos with pagination."""
    db_camera: CameraSchema | None = crud_camera.get_camera(db_session, id)
    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found!")

    return crud_video.get_video_entries(
        db_session,
        camera_ids=[db_camera.id],
        skip=pagination.page_index * pagination.page_size,
        limit=pagination.page_size,
    )
