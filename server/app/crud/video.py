"""File containing crud functions related to the Video table."""

from sqlalchemy.orm import Session

from app.api_schemas import VideoCreate, VideoUpdate
from app.crud.camera import get_camera
from app.db_models import Camera, Video


def get_video_entry(db: Session, video_id: int) -> Video | None:
    """Queries the database to get a video entry using the given ID."""
    return db.query(Video).filter(Video.id == video_id).first()


def get_video_entries_by_file_name(db: Session, file_name: str, skip: int = 0, limit: int = 100) -> list[Video]:
    """Searches for video entries that match the file name."""
    return db.query(Video).filter(Video.file_name == file_name).offset(skip).limit(limit).all()


def get_video_entries_by_cameras(db: Session, camera_ids: list[int], skip: int = 0, limit: int = 100) -> list[Video]:
    """Searches for video entries that was produced by the given camera."""
    return db.query(Video).filter(Video.camera_id.in_(camera_ids)).offset(skip).limit(limit).all()


def get_video_entries(db: Session, video_ids: list[int] | None = None, skip: int = 0, limit: int = 100) -> list[Video]:
    """Queries and returns a list of all videos with pagination.

    If a list of IDs were given, it will only return the given videos (if they were found).
    Otherwise, it returns all videos in the database (with pagination of course).
    """
    if not video_ids:
        return db.query(Video).offset(skip).limit(limit).all()
    return db.query(Video).filter(Video.id.in_(video_ids)).offset(skip).limit(limit).all()


def create_video_entry(db: Session, video: VideoCreate) -> Video | None:
    """Creates a new video entry using the given inputs."""
    # Check if the camera exists before creating the video entry
    db_camera: Camera | None = get_camera(db, video.camera_id)
    if not db_camera:
        return None

    db_video = Video(file_name=video.file_name, camera_id=db_camera.id)

    db.add(db_video)
    db.commit()
    db.refresh(db_video)

    return db_video


def update_video_entry(db: Session, video_id: int, new_video_data: VideoUpdate) -> Video | None:
    """Modifies a given video entry's parameters (excluding ID) via a given ID.

    You can only modify the name of the video for now.
    """
    # Skip modifying the database if inputs are empty
    if not new_video_data.model_fields_set:
        return None

    db_video: Video | None = get_video_entry(db, video_id)
    # Skip modifying the database if video doesn't exist
    if not db_video:
        return db_video

    if new_video_data.file_name:
        db_video.file_name = new_video_data.file_name

    db.commit()
    db.refresh(db_video)

    return db_video


def delete_video_entry(db: Session, video_id: int) -> Video | None:
    """Deletes a given video entry via ID."""
    db_video = db.query(Video).filter(Video.id == video_id).first()

    if db_video:
        db.delete(db_video)
        db.commit()

    return db_video
