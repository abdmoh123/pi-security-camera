"""File containing crud functions related to the Camera table."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.models.cameras import CameraCreate, CameraUpdate
from app.db.db_models import Camera


def get_camera(db: Session, camera_id: int) -> Camera | None:
    """Queries the database to get a camera using the given ID."""
    return db.query(Camera).filter(Camera.id == camera_id).first()


def get_cameras(
    db: Session,
    camera_ids: list[int] | None = None,
    camera_name: str | None = None,
    host_address: str | None = None,
    mac_address: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Camera]:
    """Queries and returns a list of cameras with pagination.

    It allows filtering by likeness as well as limiting the results to specifc cameras by IDs.
    """
    query = select(Camera)

    if camera_ids:
        query = query.where(Camera.id.in_(camera_ids))
    if camera_name:
        query = query.where(Camera.name.ilike(f"%{camera_name}%"))
    if host_address:
        query = query.where(Camera.host_address.ilike(f"%{host_address}%"))
    if mac_address:
        query = query.where(Camera.mac_address.ilike(f"%{mac_address}%"))

    return list(db.execute(query.offset(skip).limit(limit)).scalars().all())


def create_camera(db: Session, camera: CameraCreate) -> Camera:
    """Creates a new camera using the given inputs."""
    db_camera = Camera(
        name=camera.name, host_address=camera.host_address, auth_key=camera.auth_key, mac_address=camera.mac_address
    )

    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)

    return db_camera


def update_camera(db: Session, camera_id: int, camera: CameraUpdate) -> Camera | None:
    """Modifies a given camera's parameters (excluding ID) via a given ID."""
    db_camera = db.query(Camera).filter(Camera.id == camera_id).first()

    # skip modifying the database if inputs are empty or if camera doesn't exist
    if not camera.model_fields_set or not db_camera:
        return db_camera

    db_camera_ip = db.query(Camera).filter(Camera.host_address == camera.host_address).all()
    if db_camera_ip:
        return db_camera

    # fields left as None will not be included in the dictionary
    camera_as_dict = camera.model_dump(exclude_unset=True)

    for key, value in camera_as_dict.items():  # pyright: ignore[reportAny]
        setattr(db_camera, key, value)
    db.commit()
    db.refresh(db_camera)

    return db_camera


def delete_camera(db: Session, camera_id: int) -> Camera | None:
    """Deletes a given camera via ID."""
    db_camera = db.query(Camera).filter(Camera.id == camera_id).first()

    if db_camera:
        db.delete(db_camera)
        db.commit()

    return db_camera
