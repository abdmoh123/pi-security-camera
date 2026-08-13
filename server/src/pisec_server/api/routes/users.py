"""FastAPI routes related to the User table."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from pisec_server.api.models.camera_credentials import CameraCredentialResponse
from pisec_server.api.models.camera_subscriptions import CameraSubscription
from pisec_server.api.models.general import PaginationParams
from pisec_server.api.models.users import UserCreate, UserResponse, UserUpdate
from pisec_server.api.models.videos import Video
from pisec_server.auth import services as auth_service
from pisec_server.auth.dependencies import get_current_admin_user, get_current_user
from pisec_server.core.exceptions import RecordAlreadyExistsError, RecordNotFoundError
from pisec_server.db.database import get_db
from pisec_server.db.db_models import User as UserSchema
from pisec_server.db.db_models import Video as VideoSchema
from pisec_server.services import camera as camera_service
from pisec_server.services import camera_credential as credential_service
from pisec_server.services import camera_subscription as subscription_service
from pisec_server.services import user as user_service
from pisec_server.services import video as video_service

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
    user_id: Annotated[list[int] | None, Query()] = None,  # Named in singular form due to how it's queried
) -> list[UserSchema]:
    """Gets a list of all users with pagination. Admin only."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return user_service.get_users(
        db_session, user_id, skip=pagination.page_index * pagination.page_size, limit=pagination.page_size
    )


@router.post("/", response_model=UserResponse)
def create_user(
    user: Annotated[UserCreate, Body()],
    db_session: Annotated[Session, Depends(get_db)],
) -> UserSchema:
    """Creates a new user with given details.

    The first registered user will automatically be made an admin.
    """
    try:
        db_user: UserSchema = user_service.create_user(db_session, user)
    except RecordAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return db_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    user_id: Annotated[int, Path(ge=1)],
    db_session: Annotated[Session, Depends(get_db)],
) -> UserSchema:
    """Returns a user's details using a given ID or email."""
    # Only allow admins to view other users' details
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_user: UserSchema | None = user_service.get_user(db_session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    user_id: Annotated[int, Path(ge=1)],
    user: Annotated[UserUpdate, Body()],
    db_session: Annotated[Session, Depends(get_db)],
) -> UserSchema:
    """Updates a user's details using a given ID or email."""
    # Only allow admins to update other users' details
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    try:
        updated_user = user_service.update_user(db_session, user_id, user)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return updated_user


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
    current_user: Annotated[UserSchema, Depends(get_current_admin_user)],
    user_id: Annotated[int, Path(ge=1)],
    db_session: Annotated[Session, Depends(get_db)],
) -> UserSchema:
    """Deletes a given user by ID or email. Only Admin can delete other users."""
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # TODO: Delete all cameras and credentials before deleting the user

    # Revoke refresh tokens before deleting the user
    refresh_tokens = auth_service.revoke_all_user_refresh_tokens(db_session, user_id)

    try:
        deleted_user: UserSchema = user_service.delete_user(db_session, user_id=user_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return deleted_user


@router.post("/{user_id}/subscriptions/{camera_id}", response_model=CameraSubscription)
def create_camera_subscription(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    user_id: Annotated[int, Path(ge=1)],
    camera_id: Annotated[int, Path(ge=1)],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSubscription:
    """Subscribes a given user to a given camera that is owned by the current user."""
    # Removes camera IDs that don't exist or that aren't owned by the current user silently
    available_camera_ids: set[int] = {
        credential.camera_id for credential in current_user.credentials if credential.camera_id is not None
    }

    # Users can only subscribe other users to cameras they own, admins can do it for anyone
    if not current_user.is_admin and camera_id not in available_camera_ids:
        raise HTTPException(status_code=403, detail=f"Camera {camera_id} is not owned by the current user!")

    try:
        result: list[CameraSubscription] = subscription_service.create_camera_subscriptions_by_user(
            db_session, user_id, [camera_id]
        )
    except RecordAlreadyExistsError as e:
        raise HTTPException(status_code=409) from e
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404) from e

    return result[0]


@router.post("/{user_id}/subscriptions/", response_model=list[CameraSubscription])
def create_camera_subscriptions(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    user_id: Annotated[int, Path(ge=1)],
    camera_id: Annotated[list[int], Query(ge=1)],  # Named in singular form due to how it's queried
    db_session: Annotated[Session, Depends(get_db)],
) -> list[CameraSubscription]:
    """Subscribes a given user to given cameras that are owned by the current user."""
    # Removes camera IDs that aren't owned by the current user silently
    available_camera_ids: set[int] = {
        credential.camera_id for credential in current_user.credentials if credential.camera_id is not None
    }
    unowned_camera_ids = set(camera_id) - available_camera_ids

    # Users can only subscribe cameras they own, admins can do it for anyone
    if not current_user.is_admin and unowned_camera_ids:
        raise HTTPException(
            status_code=403, detail=f"Following cameras are not owned by the current user: {unowned_camera_ids}"
        )

    try:
        return subscription_service.create_camera_subscriptions_by_user(db_session, user_id, camera_id)
    except RecordAlreadyExistsError as e:
        raise HTTPException(status_code=409) from e
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404) from e


@router.delete("/{user_id}/subscriptions/{camera_id}", response_model=CameraSubscription)
def unsubscribe_from_camera(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    user_id: Annotated[int, Path(ge=1)],
    camera_id: Annotated[int, Path(ge=1)],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSubscription:
    """Unsubscribes a user from a given camera."""
    available_camera_ids: set[int] = {
        credential.camera_id for credential in current_user.credentials if credential.camera_id is not None
    }

    # Users can only unsubscribe cameras from themselves, admins can do it for anyone
    if not current_user.is_admin and current_user.id != user_id and camera_id not in available_camera_ids:
        raise HTTPException(status_code=403, detail=f"User {current_user.id} doesn't own {camera_id}")

    affected_user = user_service.get_user(db_session, user_id)
    if not affected_user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found!")

    if affected_user.id == current_user.id:
        subscribed_cameras: set[int] = {camera.id for camera in affected_user.cameras}
        if camera_id not in subscribed_cameras:
            raise HTTPException(status_code=404, detail=f"User {user_id} is not subscribed to {camera_id}")

    try:
        result: list[CameraSubscription] = subscription_service.delete_camera_subscriptions_by_user(
            db_session, user_id, [camera_id]
        )
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404) from e

    return result[0]


@router.delete("/{user_id}/subscriptions/", response_model=list[CameraSubscription])
def unsubscribe_from_cameras(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    user_id: Annotated[int, Path(ge=1)],
    camera_id: Annotated[list[int], Query(ge=1)],  # Named in singular form due to how it's queried
    db_session: Annotated[Session, Depends(get_db)],
) -> list[CameraSubscription]:
    """Unsubscribes a given user from given cameras."""
    # Removes camera IDs that aren't owned by the current user silently
    available_camera_ids: set[int] = {
        credential.camera_id for credential in current_user.credentials if credential.camera_id is not None
    }
    unowned_camera_ids = set(camera_id) - available_camera_ids

    # Users can only unsubscribe other users from cameras they own, admins can do it for anyone
    if not current_user.is_admin and current_user.id != user_id and unowned_camera_ids:
        raise HTTPException(
            status_code=403, detail=f"Following cameras are not owned by the current user: {unowned_camera_ids}"
        )

    # Quick exit if given user doesn't exist
    affected_user = user_service.get_user(db_session, user_id)
    if not affected_user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found!")

    # All users can unsubscribe to cameras they are subscribed to
    if affected_user.id == current_user.id:
        subscribed_camera_ids: set[int] = {camera.id for camera in affected_user.cameras}
        unsubbed_camera_ids = set(camera_id) - subscribed_camera_ids
        if unsubbed_camera_ids:
            raise HTTPException(status_code=403, detail=f"You are not subscribed to cameras: {unsubbed_camera_ids}")

    # Check if all cameras exist
    camera_ids: set[int] = {camera.id for camera in camera_service.get_cameras(db_session, camera_ids=camera_id)}
    missing_camera_ids = set(camera_id) - camera_ids
    if missing_camera_ids:
        raise HTTPException(status_code=404, detail=f"Following cameras were not found: {missing_camera_ids}")

    try:
        return subscription_service.delete_camera_subscriptions_by_user(db_session, user_id, camera_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404) from e


@router.get("/{user_id}/videos", response_model=list[Video])
def get_videos(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    user_id: Annotated[int, Path(ge=1)],
    pagination: Annotated[PaginationParams, Query()],
    db_session: Annotated[Session, Depends(get_db)],
) -> list[VideoSchema]:
    """Gets a list of all accessible videos with pagination."""
    # Users can only view their own videos, admins can view anyone's videos
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_user: UserSchema | None = user_service.get_user(db_session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    camera_ids: list[int] = [camera.id for camera in db_user.cameras]
    return video_service.get_video_entries(
        db_session, camera_ids=camera_ids, skip=pagination.page_index * pagination.page_size, limit=pagination.page_size
    )


@router.post("/{user_id}/credential", response_model=CameraCredentialResponse)
def create_credential(
    current_user: Annotated[UserSchema, Depends(get_current_admin_user)],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraCredentialResponse:
    """Creates a new credential for a given user."""
    if not user_service.get_user(db_session, current_user.id):
        raise HTTPException(status_code=404, detail="User not found!")

    new_credential = credential_service.generate_credential(current_user)
    try:
        result = credential_service.create_credential(db_session, current_user.id, new_credential)
        # Result secret is hashed, so the value from the pydantic model is used
        return CameraCredentialResponse(
            client_id=result.client_id, user_id=result.user_id, client_secret=new_credential.client_secret
        )
    except RecordAlreadyExistsError as e:
        raise HTTPException(status_code=409) from e
