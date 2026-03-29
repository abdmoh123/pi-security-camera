"""FastAPI routes related to the Camera table."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.api.models.camera_subscriptions import CameraSubscription
from app.api.models.cameras import CameraCreate, CameraResponse, CameraUpdate
from app.api.models.general import PaginationParams
from app.api.models.users import UserResponse
from app.api.models.videos import Video
from app.auth.dependencies import get_current_credential, get_current_user
from app.core.validation.regex import camera_name_regex, host_address_regex, mac_address_regex
from app.db.database import get_db
from app.db.db_models import Camera as CameraSchema
from app.db.db_models import CameraCredential as CameraCredentialSchema
from app.db.db_models import User as UserSchema
from app.db.db_models import Video as VideoSchema
from app.services import camera as camera_service
from app.services import camera_credential as camera_credential_service
from app.services import camera_subscription as subscription_service
from app.services import user as user_service
from app.services import video as video_service

router = APIRouter(prefix="/cameras", tags=["cameras"])


@router.get("/", response_model=list[CameraResponse])
def get_cameras(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    pagination: Annotated[PaginationParams, Query()],
    db_session: Annotated[Session, Depends(get_db)],
    id: Annotated[list[int] | None, Query(ge=1)] = None,
    name: Annotated[str | None, Query(regex=camera_name_regex)] = None,
    host_address: Annotated[str | None, Query(regex=host_address_regex)] = None,
    mac_address: Annotated[str | None, Query(regex=mac_address_regex)] = None,
) -> list[CameraSchema]:
    """Gets a list of all cameras with pagination.

    Non-admin users can only see cameras they are subscribed to.
    """
    cameras = camera_service.get_cameras(
        db_session,
        id,
        name,
        host_address,
        mac_address,
        pagination.page_index * pagination.page_size,
        pagination.page_size,
    )

    if not current_user.is_admin:
        # Filter to only show cameras the user is subscribed to
        subscribed_camera_ids = {camera.id for camera in current_user.cameras}
        cameras = [camera for camera in cameras if camera.id in subscribed_camera_ids]

    return cameras


@router.post("/", response_model=CameraResponse)
def create_camera(
    current_credential: Annotated[CameraCredentialSchema, Depends(get_current_credential)],
    camera: Annotated[CameraCreate, Body()],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSchema:
    """Creates a new camera with given details."""
    if current_credential.camera_id is not None:
        raise HTTPException(status_code=400, detail="Credential already linked to Camera!")

    credential_owner: UserSchema | None = user_service.get_user(db_session, current_credential.user_id)
    if not credential_owner:
        raise HTTPException(status_code=500, detail="Camera credential somehow not registered to user!")

    # Create a new camera record along with an initial subscription (to user owner of credential)
    new_camera: CameraSchema = camera_service.create_camera(db_session, camera)
    init_subscription: list[CameraSubscription] = subscription_service.create_camera_subscriptions_by_camera(
        db_session, new_camera.id, [credential_owner.id]
    )
    if len(init_subscription) != 1:
        raise HTTPException(status_code=500, detail="Failed to create camera subscription!")

    # Add the newly created camera to the credential
    modified_credential: CameraCredentialSchema | None = camera_credential_service.assign_camera(
        db_session, current_credential.client_id, new_camera.id
    )
    if not modified_credential:
        raise HTTPException(status_code=500, detail="Failed to assign camera to user!")

    return new_camera


@router.get("/{id}", response_model=CameraResponse)
def get_camera(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    id: Annotated[int, Path(ge=1)],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSchema:
    """Returns a camera's details using a given ID."""
    db_camera: CameraSchema | None = camera_service.get_camera(db_session, id)

    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found!")

    # Only allow access if user is subscribed to the camera or is an admin
    if not current_user.is_admin and db_camera not in current_user.cameras:
        raise HTTPException(status_code=403, detail="Not subscribed to this camera")

    return db_camera


@router.put("/{id}", response_model=CameraResponse)
def update_camera(
    current_credential: Annotated[CameraCredentialSchema, Depends(get_current_credential)],
    id: Annotated[int, Path(ge=1)],
    camera: Annotated[CameraUpdate, Body()],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSchema:
    """Updates a camera's details using a given ID."""
    if current_credential.camera_id is None:
        raise HTTPException(status_code=403, detail="No camera linked to credential!")
    if current_credential.camera_id != id:
        raise HTTPException(status_code=403, detail="Not authorized to update this camera!")

    if camera.host_address:
        cameras_by_ip: list[CameraSchema] = camera_service.get_cameras(
            db_session, host_address=camera.host_address, limit=1
        )
        if cameras_by_ip and cameras_by_ip[0].id != id:
            raise HTTPException(status_code=409, detail="Failed to change Host address: Already in use!")

    db_camera: CameraSchema | None = camera_service.update_camera(db_session, id, camera)
    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found!")

    return db_camera


@router.delete("/{id}", response_model=CameraResponse)
def delete_camera(
    current_credential: Annotated[CameraCredentialSchema, Depends(get_current_credential)],
    id: Annotated[int, Path(ge=1)],
    db_session: Annotated[Session, Depends(get_db)],
) -> CameraSchema:
    """Deletes a given camera by ID."""
    if current_credential.camera_id is None:
        raise HTTPException(status_code=403, detail="No camera linked to credential!")
    if current_credential.camera_id != id:
        raise HTTPException(status_code=403, detail="Not authorized to update this camera!")

    db_camera: CameraSchema | None = camera_service.delete_camera(db_session, camera_id=id)
    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    return db_camera


@router.get("/{id}/videos", response_model=list[Video])
def get_videos(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    id: Annotated[int, Path(ge=1)],
    pagination: Annotated[PaginationParams, Query()],
    db_session: Annotated[Session, Depends(get_db)],
) -> list[VideoSchema]:
    """Gets a list of all of a camera's videos with pagination."""
    db_camera: CameraSchema | None = camera_service.get_camera(db_session, id)
    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found!")

    # Only allow access if user is subscribed to the camera or is an admin
    if not current_user.is_admin and db_camera not in current_user.cameras:
        raise HTTPException(status_code=403, detail="Not subscribed to this camera")

    return video_service.get_video_entries(
        db_session,
        camera_ids=[db_camera.id],
        skip=pagination.page_index * pagination.page_size,
        limit=pagination.page_size,
    )


@router.get("/{id}/users", response_model=list[UserResponse])
def get_users(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    id: Annotated[int, Path(ge=1)],
    db_session: Annotated[Session, Depends(get_db)],
) -> list[UserSchema]:
    """Gets a list of all of a camera's users with pagination."""
    db_camera: CameraSchema | None = camera_service.get_camera(db_session, id)
    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found!")

    # Only allow access if user is subscribed to the camera or is an admin
    if not current_user.is_admin and db_camera not in current_user.cameras:
        raise HTTPException(status_code=403, detail="Not subscribed to this camera")

    return user_service.get_users(db_session, camera_ids=[id])
