"""FastAPI routes related to the User table."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from pisec_server.api.models.camera_credentials import CameraCredentialRedactedResponse, CameraCredentialResponse
from pisec_server.api.models.camera_subscriptions import CameraSubscription
from pisec_server.api.models.cameras import CameraResponse
from pisec_server.api.models.paginated.generic import PaginatedParams, PaginatedResponse
from pisec_server.api.models.paginated.user import SelfGetCamerasParams, UserGetParams
from pisec_server.api.models.users import UserCreate, UserResponse, UserUpdate
from pisec_server.api.models.videos import VideoResponse
from pisec_server.auth import services as auth_service
from pisec_server.auth.dependencies import get_current_admin_user, get_current_user
from pisec_server.core.exceptions import InvalidFileNameError, RecordAlreadyExistsError, RecordNotFoundError
from pisec_server.core.validation.video_validation import get_video_file_path_safe
from pisec_server.db.database import get_db
from pisec_server.db.db_models import CameraSubscription as CameraSubscriptionSchema
from pisec_server.db.db_models import User as UserSchema
from pisec_server.db.db_models import Video as VideoSchema
from pisec_server.services import camera as camera_service
from pisec_server.services import camera_credential as credential_service
from pisec_server.services import camera_subscription as subscription_service
from pisec_server.services import user as user_service
from pisec_server.services import video as video_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_self(current_user: Annotated[UserSchema, Depends(get_current_user)]) -> UserSchema:
    """Returns the currently authenticated user."""
    return current_user


@router.get("/me/cameras", response_model=PaginatedResponse[CameraResponse])
def get_self_cameras(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(get_db)],
    params: Annotated[SelfGetCamerasParams, Query()],
) -> PaginatedResponse[CameraResponse]:
    """Returns a user's subscribed cameras."""
    # TODO: Add sorting support
    cameras = camera_service.get_cameras(
        db_session,
        user_ids=[current_user.id],
        skip=params.page_index * params.page_size,
        limit=params.page_size,
    )

    # Filter only owned cameras
    if params.only_owned:
        cameras = [c for c in cameras if c.credential in current_user.credentials]

    camera_responses = [c.to_response() for c in cameras]
    return PaginatedResponse[CameraResponse].create(camera_responses, params.page_index, params.page_size, len(cameras))


@router.put("/me", response_model=UserResponse)
def update_self(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(get_db)],
    user: Annotated[UserUpdate, Body()],
) -> UserSchema:
    """Updates a user's details using a given ID or email."""
    try:
        updated_user = user_service.update_user(db_session, current_user.id, user)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return updated_user


@router.delete("/me", response_model=UserResponse)
def delete_self(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(get_db)],
) -> UserSchema:
    """Deletes a user's self."""
    return delete_user(current_user, db_session, current_user.id)


@router.get("/", response_model=PaginatedResponse[UserResponse])
def get_users(
    current_user: Annotated[UserSchema, Depends(get_current_user)],  # pyright: ignore[reportUnusedParameter]
    db_session: Annotated[Session, Depends(get_db)],
    params: Annotated[UserGetParams, Query()],
) -> PaginatedResponse[UserResponse]:
    """Gets a list of users with pagination."""
    users = [
        user.to_response()
        for user in user_service.get_users(
            db_session,
            params.user_id,
            params.email,
            params.camera_id,
            skip=params.page_index * params.page_size,
            limit=params.page_size,
            order_by=params.order_by.field,
            ascending=params.order_by.ascending,
        )
    ]

    return PaginatedResponse[UserResponse].create(users, params.page_index, params.page_size, len(users))


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
    db_session: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Path(ge=1)],
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
    db_session: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Path(ge=1)],
    user: Annotated[UserUpdate, Body()],
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
    db_session: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Path(ge=1)],
) -> UserSchema:
    """Deletes a given user by ID or email. Only Admin can delete other users."""
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_user: UserSchema | None = user_service.get_user(db_session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    # Delete a user's camera subscriptions
    _ = subscription_service.delete_camera_subscriptions(db_session, user_ids=[user_id])
    # Delete a user's owned cameras and credentials
    for credential in db_user.credentials:
        # Credential has the camera ID as a foreign key so it needs to be deleted first
        deleted_credential = credential_service.delete_credential(db_session, credential.client_id)
        if deleted_credential.camera_id is not None:
            # Unsubscribe all other users from the camera
            _ = subscription_service.delete_camera_subscriptions(db_session, camera_ids=[deleted_credential.camera_id])
            # Delete the camera and its videos
            _ = delete_videos(current_user, db_session, user_id=user_id, camera_id=[deleted_credential.camera_id])
            _ = camera_service.delete_camera(db_session, deleted_credential.camera_id)

    # Revoke refresh tokens before deleting the user
    _ = auth_service.revoke_all_user_refresh_tokens(db_session, user_id)

    try:
        deleted_user: UserSchema = user_service.delete_user(db_session, user_id=user_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return deleted_user


@router.post("/{user_id}/subscriptions/{camera_id}", response_model=CameraSubscription)
def create_camera_subscription(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Path(ge=1)],
    camera_id: Annotated[int, Path(ge=1)],
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
    db_session: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Path(ge=1)],
    camera_id: Annotated[list[int], Query(ge=1)],  # Named in singular form due to how it's queried
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
    db_session: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Path(ge=1)],
    camera_id: Annotated[int, Path(ge=1)],
) -> CameraSubscriptionSchema:
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
        result: list[CameraSubscriptionSchema] = subscription_service.delete_camera_subscriptions(
            db_session, [user_id], [camera_id]
        )
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404) from e

    return result[0]


@router.delete("/{user_id}/subscriptions/", response_model=list[CameraSubscription])
def unsubscribe_from_cameras(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Path(ge=1)],
    camera_id: Annotated[list[int], Query(ge=1)],  # Named in singular form due to how it's queried
) -> list[CameraSubscriptionSchema]:
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

    try:
        return subscription_service.delete_camera_subscriptions(db_session, [user_id], camera_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404) from e


@router.get("/{user_id}/videos", response_model=PaginatedResponse[VideoResponse])
def get_videos(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Path(ge=1)],
    pagination: Annotated[PaginatedParams, Query()],
) -> PaginatedResponse[VideoResponse]:
    """Gets a list of all accessible videos with pagination."""
    # Users can only view their own videos, admins can view anyone's videos
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_user: UserSchema | None = user_service.get_user(db_session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    camera_ids: list[int] = [camera.id for camera in db_user.cameras]
    videos = [
        v.to_response()
        # TODO: Add sorting support
        for v in video_service.get_video_entries(
            db_session,
            camera_ids=camera_ids,
            skip=pagination.page_index * pagination.page_size,
            limit=pagination.page_size,
        )
    ]

    return PaginatedResponse[VideoResponse].create(videos, pagination.page_index, pagination.page_size, len(videos))


@router.delete("/{user_id}/videos", response_model=VideoResponse)
def delete_videos(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Path(ge=1)],
    video_id: Annotated[list[int] | None, Query()] = None,
    camera_id: Annotated[list[int] | None, Query()] = None,
) -> list[VideoSchema]:
    """Deletes a list of videos based on the user ID."""
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_user: UserSchema | None = user_service.get_user(db_session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    if video_id is None:
        video_id = []
    if camera_id is None:
        camera_id = []

    # Filter out videos the user doesn't have access to
    available_camera_ids = {camera.id for camera in db_user.cameras}
    filtered_camera_ids = {c_id for c_id in camera_id if c_id in available_camera_ids}
    allowed_videos = video_service.get_video_entries(db_session, camera_ids=list(filtered_camera_ids))
    allowed_video_ids = {v.id for v in allowed_videos}
    filtered_video_ids = {v_id for v_id in video_id if v_id in allowed_video_ids}

    # Delete the video entries
    deleted_videos = video_service.delete_video_entries(db_session, video_ids=list(filtered_video_ids))

    # Delete the video files
    # TODO: Undo the video entry deletion if something went wrong with deleting the file
    try:
        for deleted_video in deleted_videos:
            file_path = get_video_file_path_safe(deleted_video.file_name, deleted_video.camera_id)
            file_path.unlink()
    except InvalidFileNameError as e:
        raise HTTPException(status_code=500, detail="Invalid file path!") from e
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail="Failed to delete: Video not found!") from e

    return deleted_videos


@router.get("/me/credentials", response_model=PaginatedResponse[CameraCredentialRedactedResponse])
def get_credentials(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginatedParams, Query()],
) -> PaginatedResponse[CameraCredentialRedactedResponse]:
    """Gets a user's credentials."""
    if not user_service.get_user(db_session, current_user.id):
        raise HTTPException(status_code=404, detail="User not found!")

    credentials = [
        c.to_response()
        for c in credential_service.get_credentials(
            db_session, current_user.id, skip=pagination.page_index * pagination.page_size, limit=pagination.page_size
        )
    ]

    # TODO: Get the actual total items
    return PaginatedResponse[CameraCredentialRedactedResponse].create(
        credentials, pagination.page_index, pagination.page_size, len(credentials)
    )


@router.post("/me/credentials", response_model=CameraCredentialResponse)
def create_credential(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
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


@router.delete("/me/credentials/{client_id}", response_model=CameraCredentialRedactedResponse)
def delete_credential(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(get_db)],
    client_id: Annotated[str, Path()],
) -> CameraCredentialRedactedResponse:
    """Deletes a given camera credential by ID.

    A user can only delete their own credentials.
    Once a credential is deleted, a camera using it will no longer work and may
    require setting up again.
    """
    if client_id not in [c.client_id for c in current_user.credentials]:
        # Intentionally not telling the user if credential is owned by another user
        raise HTTPException(status_code=404, detail="Credential not found!")

    try:
        result = credential_service.delete_credential(db_session, client_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404) from e

    return result.to_response()
