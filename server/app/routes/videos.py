"""FastAPI routes related to the Video table."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api_schemas import VideoCreate, VideoUpdate, Video
from app.database import get_db
from app.crud import video as crud_video
from app.db_models import Video as VideoSchema


router = APIRouter(prefix="/videos", tags=["videos"])


# TODO: Add functionality for managing the video files (e.g. deleting an entry should also delete the actual file)


@router.get("/", response_model=list[Video])
def get_videos(page_index: int = 0, page_size: int = 100, db_session: Session = Depends(get_db)) -> list[VideoSchema]:  # pyright: ignore[reportCallInDefaultInitializer]
    """Gets a list of all videos with pagination."""
    return crud_video.get_video_entries(db_session, skip=page_index * page_size, limit=page_size)


@router.post("/", response_model=Video)
def create_video(video: VideoCreate, db_session: Session = Depends(get_db)) -> VideoSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Creates a new video with the given details."""
    db_videos: list[VideoSchema] = crud_video.get_video_entries_by_file_name(db_session, video.file_name)

    for found_video in db_videos:
        if found_video.camera_id == video.camera_id:
            raise HTTPException(status_code=400, detail="Video already exists!")

    return crud_video.create_video_entry(db_session, video)


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
    """Deletes a given video by ID."""
    db_video: VideoSchema | None = crud_video.delete_video_entry(db_session, video_id=video_id)

    if not db_video:
        raise HTTPException(status_code=404, detail="Video not found")

    return db_video
