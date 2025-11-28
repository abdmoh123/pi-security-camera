"""FastAPI routes related to the User table."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api_schemas import CameraSubscription, UserCreate, UserUpdate, UserResponse
from app.database import get_db
from app.crud import user as crud_user, camera as crud_camera, camera_subscription as crud_subscription
from app.db_models import Camera, User as UserSchema


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
def get_users(page_index: int = 0, page_size: int = 100, db_session: Session = Depends(get_db)) -> list[UserSchema]:  # pyright: ignore[reportCallInDefaultInitializer]
    """Gets a list of all users with pagination."""
    return crud_user.get_users(db_session, skip=page_index * page_size, limit=page_size)


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db_session: Session = Depends(get_db)) -> UserSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Creates a new user with the given details."""
    db_user: UserSchema | None = crud_user.get_user_by_email(db_session, user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="User already exists!")

    db_user = crud_user.create_user(db_session, user)
    return db_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db_session: Session = Depends(get_db)) -> UserSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Returns a user's details using a given ID."""
    db_user: UserSchema | None = crud_user.get_user(db_session, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db_session: Session = Depends(get_db)) -> UserSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Updates a user's details using a given ID."""
    db_user: UserSchema | None = crud_user.update_user(db_session, user_id, user)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    return db_user


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db_session: Session = Depends(get_db)) -> UserSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Deletes a given user by ID."""
    db_user: UserSchema | None = crud_user.delete_user(db_session, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@router.post("/{user_id}/subscriptions/{camera_id}", response_model=CameraSubscription)
def create_camera_subscription(
    user_id: int,
    camera_id: int,
    db_session: Session = Depends(get_db),  # pyright: ignore[reportCallInDefaultInitializer]
) -> CameraSubscription:
    """Subscribes a given user to a given camera."""
    if not crud_user.get_user(db_session, user_id):
        raise HTTPException(status_code=404, detail="User not found!")

    result: list[CameraSubscription] = crud_subscription.create_camera_subscriptions_by_user(
        db_session, user_id, [camera_id]
    )
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Failed to subscribe: Camera not found!")

    return result[0]


@router.post("/{user_id}/subscriptions/", response_model=list[CameraSubscription])
def create_camera_subscriptions(
    user_id: int,
    camera_ids: list[int],
    db_session: Session = Depends(get_db),  # pyright: ignore[reportCallInDefaultInitializer]
) -> list[CameraSubscription]:
    """Subscribes a given user to the given cameras."""
    if not crud_user.get_user(db_session, user_id):
        raise HTTPException(status_code=404, detail="User not found!")

    for id in camera_ids:
        camera: Camera | None = crud_camera.get_camera(db_session, id)
        if not camera:
            raise HTTPException(status_code=404, detail=f"Failed to apply subscriptions: Camera {id} not found!")

    return crud_subscription.create_camera_subscriptions_by_user(db_session, user_id, camera_ids)


@router.delete("/{user_id}/subscriptions/{camera_id}", response_model=CameraSubscription)
def unsubscribe_from_camera(
    user_id: int,
    camera_id: int,
    db_session: Session = Depends(get_db),  # pyright: ignore[reportCallInDefaultInitializer]
) -> CameraSubscription:
    """Unsubscribes a user from a given camera."""
    if not crud_user.get_user(db_session, user_id):
        raise HTTPException(status_code=404, detail="User not found!")

    result: list[CameraSubscription] = crud_subscription.delete_camera_subscriptions_by_user(
        db_session, user_id, [camera_id]
    )
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Failed to unsubscribe: Camera not found!")

    return result[0]


@router.delete("/{user_id}/subscriptions/", response_model=list[CameraSubscription])
def unsubscribe_from_cameras(
    user_id: int,
    camera_ids: list[int],
    db_session: Session = Depends(get_db),  # pyright: ignore[reportCallInDefaultInitializer]
) -> list[CameraSubscription]:
    """Unsubscribes a given user from the given cameras."""
    if not crud_user.get_user(db_session, user_id):
        raise HTTPException(status_code=404, detail="User not found!")

    for id in camera_ids:
        camera: Camera | None = crud_camera.get_camera(db_session, id)
        if not camera:
            raise HTTPException(status_code=404, detail=f"Failed to unsubscribe: Camera {id} not found!")

    return crud_subscription.delete_camera_subscriptions_by_user(db_session, user_id, camera_ids)
