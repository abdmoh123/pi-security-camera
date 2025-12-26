"""FastAPI routes related to the Video table."""

from pathlib import Path as FilePath
from typing import Annotated

import aiofiles
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, UploadFile
from sqlalchemy.orm import Session

from app.api.models.general import PaginationParams
from app.api.models.videos import Video, VideoCreate, VideoUpdate
from app.db.database import get_db
from app.db.db_models import Camera
from app.db.db_models import Video as VideoSchema
from app.services import camera as camera_service
from app.services import video as video_service

router = APIRouter(prefix="/videos", tags=["videos"])

# TODO: Make the video files get stored on the database container instead of api server

# Make sure the path for storing the actual videos exists
VIDEO_FILES_DIR = FilePath("/var/lib/pi-security-camera/videos")
VIDEO_FILES_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/", response_model=list[Video])
def get_videos(
    pagination: Annotated[PaginationParams, Query()],
    db_session: Annotated[Session, Depends(get_db)],
    id: Annotated[list[int] | None, Query(ge=1)] = None,  # Named in singular form due to how it's queried
    file_name: Annotated[str | None, Query(min_length=5)] = None,
    camera_id: Annotated[list[int] | None, Query(ge=1)] = None,  # Named in singular form due to how it's queried
) -> list[VideoSchema]:
    """Gets a list of all videos with pagination."""
    return video_service.get_video_entries(
        db_session,
        id,
        file_name,
        camera_id,
        skip=pagination.page_index * pagination.page_size,
        limit=pagination.page_size,
    )


@router.post("/", response_model=Video)
async def upload_video(
    video_data: Annotated[VideoCreate, Body()],
    video_file: Annotated[UploadFile, Body()],
    db_session: Annotated[Session, Depends(get_db)],
) -> VideoSchema:
    """Creates and uploads a new video with the given details."""
    # Check if the video entry already exists in the database (file name and camera ID must be the same)
    db_videos: list[VideoSchema] = video_service.get_video_entries(
        db_session, file_name=video_data.file_name, camera_ids=[video_data.camera_id], limit=1
    )
    if db_videos:
        raise HTTPException(status_code=400, detail="Video already exists!")

    # Check if camera exists
    db_camera: Camera | None = camera_service.get_camera(db_session, video_data.camera_id)
    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found!")

    # Check if file uploaded is a video
    if video_file.content_type is None or "video" not in video_file.content_type:
        raise HTTPException(status_code=415, detail="File uploaded is not a video!")

    # TODO: Make it so if the file upload fails, the entry is deleted (and vice versa)

    # Create the video entry
    result_video: VideoSchema | None = video_service.create_video_entry(db_session, video_data)
    if not result_video:
        # Should never happen because the camera was checked earlier
        raise HTTPException(status_code=404, detail="Camera not found!")

    # Write the uploaded video to the server's storage (async part)
    file_path: FilePath = VIDEO_FILES_DIR / str(video_data.camera_id) / video_data.file_name
    video_contents: bytes = await video_file.read()
    async with aiofiles.open(file_path, "wb") as file:
        _ = await file.write(video_contents)

    return result_video


@router.get("/{id}", response_model=Video)
def get_video(
    id: Annotated[int, Path(ge=1)],
    db_session: Annotated[Session, Depends(get_db)],
) -> VideoSchema:
    """Returns a video's details using a given ID."""
    db_video: VideoSchema | None = video_service.get_video_entry(db_session, id)

    if not db_video:
        raise HTTPException(status_code=404, detail="Video not found!")

    return db_video


@router.put("/{id}", response_model=Video)
def update_video(
    id: Annotated[int, Path(ge=1)],
    video: Annotated[VideoUpdate, Body()],
    db_session: Annotated[Session, Depends(get_db)],
) -> VideoSchema:
    """Updates a video's details using a given ID."""
    db_video: VideoSchema | None = video_service.update_video_entry(db_session, id, video)

    if not db_video:
        raise HTTPException(status_code=404, detail="Video not found!")

    return db_video


@router.delete("/{id}", response_model=Video)
def delete_video(
    id: Annotated[int, Path(ge=1)],
    db_session: Annotated[Session, Depends(get_db)],
) -> VideoSchema:
    """Deletes the given video."""
    deleted_video: VideoSchema | None = video_service.delete_video_entry(db_session, id)
    if not deleted_video:
        raise HTTPException(status_code=404, detail="Failed to delete: Video not found!")

    # Delete the video file
    file_path: FilePath = VIDEO_FILES_DIR / str(deleted_video.camera_id) / deleted_video.file_name
    file_path.unlink()

    return deleted_video
