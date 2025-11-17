"""FastAPI routes related to the Camera table."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api_schemas import CameraCreate, CameraUpdate, Camera
from app.database import get_db
from app.crud import camera as crud_camera
from app.db_models import Camera as CameraSchema


router = APIRouter(prefix="/cameras", tags=["cameras"])


@router.get("/", response_model=list[Camera])
def get_cameras(page_index: int = 0, page_size: int = 100, db_session: Session = Depends(get_db)) -> list[CameraSchema]:  # pyright: ignore[reportCallInDefaultInitializer]
    """Gets a list of all cameras with pagination."""
    return crud_camera.get_cameras(db_session, skip=page_index * page_size, limit=page_size)


@router.post("/", response_model=Camera)
def create_camera(camera: CameraCreate, db_session: Session = Depends(get_db)) -> CameraSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Creates a new camera with the given details."""
    db_camera: CameraSchema | None = crud_camera.get_camera_by_name(db_session, camera.name)

    if db_camera:
        raise HTTPException(status_code=400, detail="Camera already exists!")

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
