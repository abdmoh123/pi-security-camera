"""FastAPI routes related to the User table."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.api.models.camera_subscriptions import CameraSubscription
from app.api.models.general import PaginationParams
from app.api.models.users import IDorEmail, UserCreate, UserResponse, UserUpdate
from app.api.models.videos import Video
from app.auth.dependencies import get_current_admin_user, get_current_user
from app.core.utils import user_matches_id_or_email
from app.db.database import get_db
from app.db.db_models import Camera
from app.db.db_models import User as UserSchema
from app.db.db_models import Video as VideoSchema
from app.services import camera as camera_service
from app.services import camera_subscription as subscription_service
from app.services import user as user_service
from app.services import video as video_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_user_me(current_user: Annotated[UserSchema, Depends(get_current_user)]) -> UserSchema:
    """Returns the currently authenticated user."""
    return current_user


@router.get("/", response_model=list[UserResponse])
def get_users(
    current_user: Annotated[UserSchema, Depends(get_current_admin_user)],
    pagination: Annotated[PaginationParams, Query()],
    db_session: Annotated[Session, Depends(get_db)],
    user: Annotated[list[int] | list[str] | None, Query()] = None,
) -> list[UserSchema]:
    """Gets a list of all users with pagination. Admin only."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return user_service.get_users(
        db_session, user, skip=pagination.page_index * pagination.page_size, limit=pagination.page_size
    )


@router.post("/", response_model=UserResponse)
def create_user(
    current_user: Annotated[UserSchema, Depends(get_current_admin_user)],
    user: Annotated[UserCreate, Body()],
    db_session: Annotated[Session, Depends(get_db)],
) -> UserSchema:
    """Creates a new user with given details. Admin only.

    The first registered user will automatically be made an admin.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_user: UserSchema | None = user_service.get_user_by_email(db_session, user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="User already exists!")

    db_user = user_service.create_user(db_session, user)
    return db_user


@router.get("/{id_or_email}", response_model=UserResponse)
def get_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    id_or_email: Annotated[IDorEmail, Path()],
    db_session: Annotated[Session, Depends(get_db)],
) -> UserSchema:
    """Returns a user's details using a given ID or email."""
    db_user: UserSchema | None = user_service.get_user(db_session, id_or_email.value)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    # Only allow admins to view other users' details
    if not current_user.is_admin and current_user.id != db_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return db_user


@router.put("/{id_or_email}", response_model=UserResponse)
def update_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    id_or_email: Annotated[IDorEmail, Path()],
    user: Annotated[UserUpdate, Body()],
    db_session: Annotated[Session, Depends(get_db)],
) -> UserSchema:
    """Updates a user's details using a given ID or email."""
    db_user: UserSchema | None = user_service.get_user(db_session, id_or_email.value)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    # Only allow admins to update other users' details
    if not current_user.is_admin and current_user.id != db_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    updated_user = user_service.update_user(db_session, id_or_email.value, user)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found!")

    return updated_user


@router.delete("/{id_or_email}", response_model=UserResponse)
def delete_user(
    current_user: Annotated[UserSchema, Depends(get_current_admin_user)],
    id_or_email: Annotated[IDorEmail, Path()],
    db_session: Annotated[Session, Depends(get_db)],
) -> UserSchema:
    """Deletes a given user by ID or email. Only Admin can delete other users."""
    db_user: UserSchema | None = user_service.get_user(db_session, id_or_email.value)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    if not current_user.is_admin and current_user.id != db_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    deleted_user: UserSchema | None = user_service.delete_user(db_session, user_id_or_email=id_or_email.value)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")

    # TODO: Revoke all tokens associated with the deleted user

    return deleted_user


@router.post("/{id_or_email}/subscriptions/{camera_id}", response_model=CameraSubscription)
def create_camera_subscription(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    id_or_email: Annotated[IDorEmail, Path()],
    camera_id: Annotated[int, Path(ge=1)],  # Named in singular form due to how it's queried
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSubscription:
    """Subscribes a given user to a given camera."""
    # Users can only subscribe cameras to themselves, admins can do it for anyone
    if not current_user.is_admin and not user_matches_id_or_email(id_or_email, current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if not user_service.get_user(db_session, id_or_email.value):
        raise HTTPException(status_code=404, detail="User not found!")

    result: list[CameraSubscription] = subscription_service.create_camera_subscriptions_by_user(
        db_session, id_or_email.value, [camera_id]
    )
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Failed to subscribe: Camera not found!")

    return result[0]


@router.post("/{id_or_email}/subscriptions/", response_model=list[CameraSubscription])
def create_camera_subscriptions(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    id_or_email: Annotated[IDorEmail, Path()],
    camera_id: Annotated[list[int], Query(ge=1)],  # Named in singular form due to how it's queried
    db_session: Annotated[Session, Depends(get_db)],
) -> list[CameraSubscription]:
    """Subscribes a given user to given cameras."""
    # Users can only subscribe cameras to themselves, admins can do it for anyone
    if not current_user.is_admin and not user_matches_id_or_email(id_or_email, current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if not user_service.get_user(db_session, id_or_email.value):
        raise HTTPException(status_code=404, detail="User not found!")

    cameras: list[Camera] = camera_service.get_cameras(db_session, camera_ids=camera_id)
    for camera in cameras:
        if camera.id not in camera_id:
            raise HTTPException(status_code=404, detail=f"Failed to apply subscriptions: Camera {camera.id} not found!")

    return subscription_service.create_camera_subscriptions_by_user(db_session, id_or_email.value, camera_id)


@router.delete("/{id_or_email}/subscriptions/{camera_id}", response_model=CameraSubscription)
def unsubscribe_from_camera(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    id_or_email: Annotated[IDorEmail, Path()],
    camera_id: Annotated[int, Path(ge=1)],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSubscription:
    """Unsubscribes a user from a given camera."""
    # Users can only unsubscribe cameras from themselves, admins can do it for anyone
    if not current_user.is_admin and not user_matches_id_or_email(id_or_email, current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if not user_service.get_user(db_session, id_or_email.value):
        raise HTTPException(status_code=404, detail="User not found!")

    result: list[CameraSubscription] = subscription_service.delete_camera_subscriptions_by_user(
        db_session, id_or_email.value, [camera_id]
    )
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Failed to unsubscribe: Camera not found!")

    return result[0]


@router.delete("/{id_or_email}/subscriptions/", response_model=list[CameraSubscription])
def unsubscribe_from_cameras(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    id_or_email: Annotated[IDorEmail, Path()],
    camera_id: Annotated[list[int], Query(ge=1)],  # Named in singular form due to how it's queried
    db_session: Annotated[Session, Depends(get_db)],
) -> list[CameraSubscription]:
    """Unsubscribes a given user from given cameras."""
    # Users can only unsubscribe cameras from themselves, admins can do it for anyone
    if not current_user.is_admin and not user_matches_id_or_email(id_or_email, current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if not user_service.get_user(db_session, id_or_email.value):
        raise HTTPException(status_code=404, detail="User not found!")

    cameras: list[Camera] = camera_service.get_cameras(db_session, camera_ids=camera_id)
    for camera in cameras:
        if camera.id not in camera_id:
            raise HTTPException(status_code=404, detail=f"Failed to unsubscribe: Camera {camera.id} not found!")

    return subscription_service.delete_camera_subscriptions_by_user(db_session, id_or_email.value, camera_id)


@router.get("/{id_or_email}/videos", response_model=list[Video])
def get_videos(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    id_or_email: Annotated[IDorEmail, Path()],
    pagination: Annotated[PaginationParams, Query()],
    db_session: Annotated[Session, Depends(get_db)],
) -> list[VideoSchema]:
    """Gets a list of all accessible videos with pagination."""
    # Users can only view their own videos, admins can view anyone's videos
    if not current_user.is_admin and not user_matches_id_or_email(id_or_email, current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_user: UserSchema | None = user_service.get_user(db_session, id_or_email.value)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    camera_ids: list[int] = [camera.id for camera in db_user.cameras]
    return video_service.get_video_entries(
        db_session, camera_ids=camera_ids, skip=pagination.page_index * pagination.page_size, limit=pagination.page_size
    )
