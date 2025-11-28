"""File containing crud functions related to the Video table."""

from sqlalchemy.orm import Session

from app.api_schemas import VideoCreate, VideoUpdate
from app.crud.camera import get_camera
from app.crud.user import get_users
from app.db_models import Camera, User, Video


def get_video_entry(db: Session, video_id: int) -> Video | None:
    """Queries the database to get a video entry using the given ID."""
    return db.query(Video).filter(Video.id == video_id).first()


def get_video_entries_by_file_name(db: Session, file_name: str, skip: int = 0, limit: int = 100) -> list[Video]:
    """Searches for video entries that match the file name."""
    return db.query(Video).filter(Video.file_name == file_name).offset(skip).limit(limit).all()


def get_video_entries(db: Session, video_ids: list[int] | None = None, skip: int = 0, limit: int = 100) -> list[Video]:
    """Queries and returns a list of all videos with pagination.

    If a list of IDs were given, it will only return the given videos (if they were found).
    Otherwise, it returns all videos in the database (with pagination of course).
    """
    if not video_ids:
        return db.query(Video).offset(skip).limit(limit).all()
    return db.query(Video).filter(Video.id.in_(video_ids)).offset(skip).limit(limit).all()


def create_video_entry(db: Session, video: VideoCreate) -> Video:
    """Creates a new video entry using the given inputs."""
    db_camera: Camera | None = None
    users: list[User] = list()
    if video.camera_id:
        db_camera = get_camera(db, video.camera_id)
        if db_camera:
            users = db_camera.users

    db_video = Video(file_name=video.file_name, camera_id=video.camera_id, users=users)

    db.add(db_video)
    db.commit()
    db.refresh(db_video)

    return db_video


def update_video_entry(db: Session, video_id: int, new_video_data: VideoUpdate) -> Video | None:
    """Modifies a given video entry's parameters (excluding ID) via a given ID.

    There are special rules for assigning users to a video:
    - If a camera is linked to the video, only the users subscribed to that camera can view the video.
        - Any passed-in user list is ignored
    - If no camera is linked, then any user can be assigned to have access to the video.
        - The passed-in users will be linked to the video
        - If the inputted camera ID = 0, then the video will have no camera linked
    """
    db_video = db.query(Video).filter(Video.id == video_id).first()

    # skip modifying the database if inputs are empty or if video doesn't exist
    if not new_video_data.model_fields_set or not db_video:
        return db_video

    if new_video_data.file_name:
        # you can't have multiple videos with the same file name (conflict issue)
        videos_with_file_name: list[Video] = get_video_entries_by_file_name(db, new_video_data.file_name)
        if not videos_with_file_name:
            db_video.file_name = new_video_data.file_name

    # a camera ID of 0 is defined as no camera (None value means don't change the camera ID)
    if new_video_data.camera_id == 0:
        db_video.camera_id = None
    # setting a new camera id should make it so only the users subscribed to the new camera can access it
    elif new_video_data.camera_id:
        camera: Camera | None = get_camera(db, new_video_data.camera_id)
        if camera:
            db_video.camera_id = camera.id
            db_video.users = camera.users
    # if the video isn't linked to a camera, the users with access don't need to be subscribed to a specific camera
    elif new_video_data.user_ids and not db_video.camera_id:
        db_video.users = get_users(db, new_video_data.user_ids)

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
