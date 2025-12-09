"""FastAPI routes related to the Video table."""

from pathlib import Path

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.models.videos import Video, VideoCreate, VideoUpdate
from app.crud import camera as crud_camera
from app.crud import video as crud_video
from app.db.database import get_db
from app.db.db_models import Camera
from app.db.db_models import Video as VideoSchema

router = APIRouter(prefix="/videos", tags=["videos"])

# TODO: Make the video files get stored on the database container instead of api server

# Make sure the path for storing the actual videos exists
VIDEO_FILES_DIR = Path("/var/lib/pi-security-camera/videos")
VIDEO_FILES_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/", response_model=list[Video])
def get_videos(
    video_ids: list[int] | None = None,
    file_name: str | None = None,
    camera_ids: list[int] | None = None,
    page_index: int = 0,
    page_size: int = 100,
    db_session: Session = Depends(get_db),  # pyright: ignore[reportCallInDefaultInitializer]
) -> list[VideoSchema]:
    """Gets a list of all videos with pagination."""
    return crud_video.get_video_entries(
        db_session, video_ids, file_name, camera_ids, skip=page_index * page_size, limit=page_size
    )


@router.post("/", response_model=Video)
async def upload_video(
    video_data: VideoCreate,
    video_file: UploadFile,
    db_session: Session = Depends(get_db),  # pyright: ignore[reportCallInDefaultInitializer]
) -> VideoSchema:
    """Creates and uploads a new video with the given details."""
    # Check if the video entry already exists in the database (file name and camera ID must be the same)
    db_videos: list[VideoSchema] = crud_video.get_video_entries(
        db_session, file_name=video_data.file_name, camera_ids=[video_data.camera_id], limit=1
    )
    if db_videos:
        raise HTTPException(status_code=400, detail="Video already exists!")

    # Check if camera exists
    db_camera: Camera | None = crud_camera.get_camera(db_session, video_data.camera_id)
    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found!")

    # Check if file uploaded is a video
    if video_file.content_type is None or "video" not in video_file.content_type:
        raise HTTPException(status_code=415, detail="File uploaded is not a video!")

    # TODO: Make it so if the file upload fails, the entry is deleted (and vice versa)

    # Create the video entry
    result_video: VideoSchema | None = crud_video.create_video_entry(db_session, video_data)
    if not result_video:
        # Should never happen because the camera was checked earlier
        raise HTTPException(status_code=404, detail="Camera not found!")

    # Write the uploaded video to the server's storage (async part)
    file_path: Path = VIDEO_FILES_DIR / str(video_data.camera_id) / video_data.file_name
    video_contents: bytes = await video_file.read()
    async with aiofiles.open(file_path, "wb") as file:
        _ = await file.write(video_contents)

    return result_video


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
def delete_video(video_id: int, db_session: Session = Depends(get_db)) -> VideoSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Deletes the given video."""
    deleted_video: VideoSchema | None = crud_video.delete_video_entry(db_session, video_id)
    if not deleted_video:
        raise HTTPException(status_code=404, detail="Failed to delete: Video not found!")

    # Delete the video file
    file_path: Path = VIDEO_FILES_DIR / str(deleted_video.camera_id) / deleted_video.file_name
    file_path.unlink()

    return deleted_video
