"""FastAPI routes related to the Video table."""

from pathlib import Path

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api_schemas import VideoCreate, VideoUpdate, Video
from app.database import get_db
from app.crud import video as crud_video
from app.db_models import Video as VideoSchema


router = APIRouter(prefix="/videos", tags=["videos"])

# Make sure the path for storing the actual videos exists
VIDEO_FILES_DIR = Path("/var/lib/pi-security-camera/videos")
VIDEO_FILES_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/", response_model=list[Video])
def get_videos(page_index: int = 0, page_size: int = 100, db_session: Session = Depends(get_db)) -> list[VideoSchema]:  # pyright: ignore[reportCallInDefaultInitializer]
    """Gets a list of all videos with pagination."""
    return crud_video.get_video_entries(db_session, skip=page_index * page_size, limit=page_size)


@router.post("/", response_model=Video)
async def upload_video(
    video_data: VideoCreate,
    video_file: UploadFile,
    db_session: Session = Depends(get_db),  # pyright: ignore[reportCallInDefaultInitializer]
) -> VideoSchema:
    """Creates and uploads a new video with the given details."""
    db_videos: list[VideoSchema] = crud_video.get_video_entries_by_file_name(db_session, video_data.file_name)

    # Check if the video entry already exists in the database
    for found_video in db_videos:
        if found_video.camera_id == video_data.camera_id:
            raise HTTPException(status_code=400, detail="Video already exists!")

    if video_file.content_type is None or "video" not in video_file.content_type:
        raise HTTPException(status_code=404, detail="File uploaded is not a video!")

    # Write the uploaded video to the server's storage (async part)
    file_path: Path = VIDEO_FILES_DIR / str(video_data.camera_id) / video_data.file_name
    video_contents: bytes = await video_file.read()
    async with aiofiles.open(file_path, "wb") as file:
        _ = await file.write(video_contents)

    return crud_video.create_video_entry(db_session, video_data)


@router.get("/{video_id}", response_model=Video)
def get_video(video_id: int, db_session: Session = Depends(get_db)) -> VideoSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Returns a video's details using a given ID."""
    db_video: VideoSchema | None = crud_video.get_video_entry(db_session, video_id)

    if not db_video:
        raise HTTPException(status_code=404, detail="Video not found!")

    return db_video


@router.put("/{video_id}", response_model=Video)
def update_video(video_id: int, video: VideoUpdate, db_session: Session = Depends(get_db)) -> VideoSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Updates a video's details using a given ID."""
    db_video: VideoSchema | None = crud_video.update_video_entry(db_session, video_id, video)

    if not db_video:
        raise HTTPException(status_code=404, detail="Video not found!")

    return db_video


@router.delete("/{video_id}", response_model=Video)
def unlink_user_from_video(video_id: int, user_id: int, db_session: Session = Depends(get_db)) -> VideoSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Unlinks a given user from a given video.

    If the last linked user was removed, then the video is deleted (no one can access it anyway).
    """
    db_video: VideoSchema | None = crud_video.get_video_entry(db_session, video_id)
    if not db_video:
        raise HTTPException(status_code=404, detail="Failed to unlink user: Video not found")

    # TODO: Make sure that you can only unlink a user if the video isn't linked to a camera
    #       Also allow unlinking a video from a camera (e.g. manually or by deleting a camera account)

    # Find and unlink the user from the video
    removed_user: bool = False
    for user in db_video.users:
        if user.id == user_id:
            removed_user = True
            db_video.users.remove(user)
            break
    if not removed_user:
        raise HTTPException(status_code=404, detail="Failed to unlink user: User not linked to video!")

    # Delete the video if no users are linked anymore
    if not db_video.users:
        # Delete the video entry
        deleted_video: VideoSchema | None = crud_video.delete_video_entry(db_session, video_id)
        # Should never be None due to the video already being found earlier
        if not deleted_video:
            raise HTTPException(status_code=404, detail="Failed to delete: Video not found!")

        # Delete the video file
        file_path: Path = VIDEO_FILES_DIR / str(db_video.camera_id) / db_video.file_name
        file_path.unlink()

        return deleted_video

    # Update the video entry with the new list of linked users
    updated_video_model = VideoUpdate.model_validate(db_video)
    updated_video: VideoSchema | None = crud_video.update_video_entry(db_session, video_id, updated_video_model)

    # Shouldn't happen because the video was already found at the beginning
    if not updated_video:
        raise HTTPException(status_code=404, detail="Failed to unlink user: Video not found")

    return updated_video
