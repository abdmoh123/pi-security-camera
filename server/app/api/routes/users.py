"""FastAPI routes related to the User table."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.api.models.camera_subscriptions import CameraSubscription
from app.api.models.general import PaginationParams
from app.api.models.users import UserCreate, UserResponse, UserUpdate
from app.api.models.videos import Video
from app.crud import camera as crud_camera
from app.crud import camera_subscription as crud_subscription
from app.crud import user as crud_user
from app.crud import video as crud_video
from app.db.database import get_db
from app.db.db_models import Camera
from app.db.db_models import User as UserSchema
from app.db.db_models import Video as VideoSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
def get_users(
    pagination: Annotated[PaginationParams, Query()],
    db_session: Annotated[Session, Depends(get_db)],
    user_list: Annotated[list[int] | list[str] | None, Query()] = None,
) -> list[UserSchema]:
    """Gets a list of all users with pagination."""
    return crud_user.get_users(
        db_session, user_list, skip=pagination.page_index * pagination.page_size, limit=pagination.page_size
    )


@router.post("/", response_model=UserResponse)
def create_user(
    user: Annotated[UserCreate, Body()],
    db_session: Annotated[Session, Depends(get_db)],
) -> UserSchema:
    """Creates a new user with the given details."""
    db_user: UserSchema | None = crud_user.get_user_by_email(db_session, user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="User already exists!")

    db_user = crud_user.create_user(db_session, user)
    return db_user


@router.get("/{id_or_email}", response_model=UserResponse)
def get_user(id_or_email: Annotated[int | str, Path()], db_session: Annotated[Session, Depends(get_db)]) -> UserSchema:
    """Returns a user's details using a given ID or email."""
    db_user: UserSchema | None = crud_user.get_user(db_session, id_or_email)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    return db_user


@router.put("/{id_or_email}", response_model=UserResponse)
def update_user(
    id_or_email: Annotated[int, Path()],
    user: Annotated[UserUpdate, Body()],
    db_session: Annotated[Session, Depends(get_db)],
) -> UserSchema:
    """Updates a user's details using a given ID or email."""
    db_user: UserSchema | None = crud_user.update_user(db_session, id_or_email, user)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    return db_user


@router.delete("/{id_or_email}", response_model=UserResponse)
def delete_user(
    id_or_email: Annotated[int, Path()],
    db_session: Annotated[Session, Depends(get_db)],
) -> UserSchema:
    """Deletes a given user by ID or email."""
    db_user: UserSchema | None = crud_user.delete_user(db_session, user_id_or_email=id_or_email)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@router.post("/{id_or_email}/subscriptions/{camera_id}", response_model=CameraSubscription)
def create_camera_subscription(
    id_or_email: Annotated[int | str, Path()],
    camera_id: Annotated[int, Path()],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSubscription:
    """Subscribes a given user to a given camera."""
    if not crud_user.get_user(db_session, id_or_email):
        raise HTTPException(status_code=404, detail="User not found!")

    result: list[CameraSubscription] = crud_subscription.create_camera_subscriptions_by_user(
        db_session, id_or_email, [camera_id]
    )
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Failed to subscribe: Camera not found!")

    return result[0]


@router.post("/{id_or_email}/subscriptions/", response_model=list[CameraSubscription])
def create_camera_subscriptions(
    id_or_email: Annotated[int | str, Path()],
    camera_ids: Annotated[list[int], Query()],
    db_session: Annotated[Session, Depends(get_db)],
) -> list[CameraSubscription]:
    """Subscribes a given user to the given cameras."""
    if not crud_user.get_user(db_session, id_or_email):
        raise HTTPException(status_code=404, detail="User not found!")

    cameras: list[Camera] = crud_camera.get_cameras(db_session, camera_ids=camera_ids)
    for camera in cameras:
        if camera.id not in camera_ids:
            raise HTTPException(status_code=404, detail=f"Failed to apply subscriptions: Camera {camera.id} not found!")

    return crud_subscription.create_camera_subscriptions_by_user(db_session, id_or_email, camera_ids)


@router.delete("/{id_or_email}/subscriptions/{camera_id}", response_model=CameraSubscription)
def unsubscribe_from_camera(
    id_or_email: Annotated[int | str, Path()],
    camera_id: Annotated[int, Path()],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSubscription:
    """Unsubscribes a user from a given camera."""
    if not crud_user.get_user(db_session, id_or_email):
        raise HTTPException(status_code=404, detail="User not found!")

    result: list[CameraSubscription] = crud_subscription.delete_camera_subscriptions_by_user(
        db_session, id_or_email, [camera_id]
    )
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Failed to unsubscribe: Camera not found!")

    return result[0]


@router.delete("/{id_or_email}/subscriptions/", response_model=list[CameraSubscription])
def unsubscribe_from_cameras(
    id_or_email: Annotated[int | str, Path()],
    camera_ids: Annotated[list[int], Query()],
    db_session: Annotated[Session, Depends(get_db)],
) -> list[CameraSubscription]:
    """Unsubscribes a given user from the given cameras."""
    if not crud_user.get_user(db_session, id_or_email):
        raise HTTPException(status_code=404, detail="User not found!")

    cameras: list[Camera] = crud_camera.get_cameras(db_session, camera_ids=camera_ids)
    for camera in cameras:
        if camera.id not in camera_ids:
            raise HTTPException(status_code=404, detail=f"Failed to unsubscribe: Camera {camera.id} not found!")

    return crud_subscription.delete_camera_subscriptions_by_user(db_session, id_or_email, camera_ids)


@router.get("/{id_or_email}/videos", response_model=list[Video])
def get_videos(
    id_or_email: Annotated[int | str, Path()],
    pagination: Annotated[PaginationParams, Query()],
    db_session: Annotated[Session, Depends(get_db)],
) -> list[VideoSchema]:
    """Gets a list of all accessible videos with pagination."""
    db_user: UserSchema | None = crud_user.get_user(db_session, id_or_email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    camera_ids: list[int] = [camera.id for camera in db_user.cameras]
    return crud_video.get_video_entries(
        db_session, camera_ids=camera_ids, skip=pagination.page_index * pagination.page_size, limit=pagination.page_size
    )
