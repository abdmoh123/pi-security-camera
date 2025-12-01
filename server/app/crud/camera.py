"""File containing crud functions related to the Camera table."""

from sqlalchemy.orm import Session

from app.api_schemas import CameraCreate, CameraUpdate
from app.db_models import Camera


def get_camera(db: Session, camera_id: int) -> Camera | None:
    """Queries the database to get a camera using the given ID."""
    return db.query(Camera).filter(Camera.id == camera_id).first()


def get_camera_by_host_address(db: Session, host_address: str) -> Camera | None:
    """Queries for a camera with the given host address (e.g. IP address).

    We can't have multiple cameras with the same IP address.
    """
    return db.query(Camera).filter(Camera.host_address == host_address).first()


def get_cameras_by_name(db: Session, name: str, skip: int = 0, limit: int = 100) -> list[Camera]:
    """Queries the database to get a list of cameras that have the given name."""
    return db.query(Camera).filter(Camera.name == name).offset(skip).limit(limit).all()


def get_cameras_by_mac_address(db: Session, mac_address: str, skip: int = 0, limit: int = 100) -> list[Camera]:
    """Queries the database to get a list of cameras that have the given MAC address."""
    return db.query(Camera).filter(Camera.mac_address == mac_address).offset(skip).limit(limit).all()


def get_cameras(db: Session, camera_ids: list[int] | None = None, skip: int = 0, limit: int = 100) -> list[Camera]:
    """Queries and returns a list of cameras with pagination.

    If a list of IDs were given, it will only return the given cameras (if they were found).
    Otherwise, it returns all cameras in the database (with pagination of course).
    """
    if not camera_ids:
        return db.query(Camera).offset(skip).limit(limit).all()
    return db.query(Camera).filter(Camera.id.in_(camera_ids)).offset(skip).limit(limit).all()


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
