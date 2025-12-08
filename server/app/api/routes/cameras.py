"""FastAPI routes related to the Camera table."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.models.cameras import Camera, CameraCreate, CameraUpdate
from app.api.models.videos import Video
from app.crud import camera as crud_camera
from app.crud import video as crud_video
from app.db.database import get_db
from app.db.db_models import Camera as CameraSchema
from app.db.db_models import Video as VideoSchema

router = APIRouter(prefix="/cameras", tags=["cameras"])


@router.get("/", response_model=list[Camera])
def get_cameras(
    camera_ids: list[int] | None = None,
    camera_name: str | None = None,
    page_index: int = 0,
    page_size: int = 100,
    db_session: Session = Depends(get_db),  # pyright: ignore[reportCallInDefaultInitializer]
) -> list[CameraSchema]:
    """Gets a list of all cameras with pagination."""
    skip: int = page_index * page_size
    if camera_name:
        # return cameras that contain the string in camera_name, not an exact match
        return crud_camera.get_cameras_by_name(db_session, camera_name, skip, limit=page_size)
    return crud_camera.get_cameras(db_session, camera_ids, skip=page_index * page_size, limit=page_size)


@router.post("/", response_model=Camera)
def create_camera(camera: CameraCreate, db_session: Session = Depends(get_db)) -> CameraSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Creates a new camera with the given details."""
    db_camera: CameraSchema | None = crud_camera.get_camera_by_host_address(db_session, camera.host_address)

    if db_camera:
        raise HTTPException(status_code=400, detail="Camera already exists: Host address is already in use!")

    db_camera = crud_camera.create_camera(db_session, camera)
    return db_camera


@router.get("/{camera_id}", response_model=Camera)
def get_camera(camera_id: int, db_session: Session = Depends(get_db)) -> CameraSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Returns a camera's details using a given ID."""
    db_camera: CameraSchema | None = crud_camera.get_camera(db_session, camera_id)

    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found!")

    return db_camera


@router.put("/{camera_id}", response_model=Camera)
def update_camera(camera_id: int, camera: CameraUpdate, db_session: Session = Depends(get_db)) -> CameraSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Updates a camera's details using a given ID."""
    if camera.host_address:
        db_camera_ip: CameraSchema | None = crud_camera.get_camera_by_host_address(db_session, camera.host_address)
        if db_camera_ip and db_camera_ip.id != camera_id:
            raise HTTPException(status_code=409, detail="Failed to change Host address: Already in use!")

    db_camera: CameraSchema | None = crud_camera.update_camera(db_session, camera_id, camera)

    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found!")

    return db_camera


@router.delete("/{camera_id}", response_model=Camera)
def delete_camera(camera_id: int, db_session: Session = Depends(get_db)) -> CameraSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Deletes a given camera by ID."""
    db_camera: CameraSchema | None = crud_camera.delete_camera(db_session, camera_id=camera_id)

    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    return db_camera


@router.get("/{camera_id}/videos", response_model=list[Video])
def get_videos(
    camera_id: int,
    page_index: int = 0,
    page_size: int = 100,
    db_session: Session = Depends(get_db),  # pyright: ignore[reportCallInDefaultInitializer]
) -> list[VideoSchema]:
    """Gets a list of all of a camera's videos with pagination."""
    db_camera: CameraSchema | None = crud_camera.get_camera(db_session, camera_id)
    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found!")

    return crud_video.get_video_entries_by_cameras(
        db_session, [db_camera.id], skip=page_index * page_size, limit=page_size
    )
