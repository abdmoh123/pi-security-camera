"""File containing crud functions related to the Video table."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from pisec_server.api.models.videos import VideoUpdate
from pisec_server.core.exceptions import RecordNotFoundError
from pisec_server.db.db_models import Camera, Video
from pisec_server.services.camera import get_camera


def get_video_entry(db: Session, video_id: int) -> Video | None:
    """Queries the database to get a video entry using the given ID."""
    return db.query(Video).filter(Video.id == video_id).first()


def get_video_entries(
    db: Session,
    video_ids: list[int] | None = None,
    file_name: str | None = None,
    camera_ids: list[int] | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Video]:
    """Queries and returns a list of videos with pagination.

    Allows filtering by likeness and also limiting results to chosen list of IDs.
    """
    query = select(Video)

    if video_ids:
        query = query.where(Video.id.in_(video_ids))
    if file_name:
        query = query.where(Video.file_name.ilike(f"%{file_name}%"))
    if camera_ids:
        query = query.where(Video.camera_id.in_(camera_ids))

    return list(db.execute(query.offset(skip).limit(limit)).scalars().all())


def create_video_entry(db: Session, file_name: str, camera_id: int) -> Video:
    """Creates a new video entry using the given inputs."""
    # Check if the camera exists before creating the video entry
    db_camera: Camera | None = get_camera(db, camera_id)
    if not db_camera:
        raise RecordNotFoundError(f"Failed to create video: Camera {camera_id} does not exist!")

    db_video = Video(file_name=file_name, camera_id=db_camera.id)

    db.add(db_video)
    db.commit()

    return db_video


def update_video_entry(db: Session, video_id: int, new_video_data: VideoUpdate) -> Video:
    """Modifies a given video entry's parameters (excluding ID) via a given ID.

    You can only modify the name of the video for now.
    """
    db_video: Video | None = get_video_entry(db, video_id)
    # Skip modifying the database if video doesn't exist
    if not db_video:
        raise RecordNotFoundError(f"Video {video_id} does not exist!")

    # Skip modifying the database if inputs are empty
    if not new_video_data.model_fields_set:
        return db_video

    if new_video_data.file_name:
        db_video.file_name = new_video_data.file_name

    db.commit()

    return db_video


def delete_video_entry(db: Session, video_id: int) -> Video:
    """Deletes a given video entry via ID."""
    db_video = db.query(Video).filter(Video.id == video_id).first()

    if not db_video:
        raise RecordNotFoundError(f"Video {video_id} does not exist!")

    db.delete(db_video)
    db.commit()

    return db_video
