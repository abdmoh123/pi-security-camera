"""FastAPI routes related to the CameraSubscription table."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api_schemas import CameraSubscription
from app.database import get_db
from app.crud import camera_subscription as crud_camera_subscription
from app.db_models import CameraSubscription as CameraSubscriptionSchema


router = APIRouter(prefix="/users/subscriptions", tags=["camera_subscriptions"])


@router.get("/", response_model=list[CameraSubscription])
def get_camera_subscriptions(
    page_index: int = 0,
    page_size: int = 100,
    db_session: Session = Depends(get_db),  # pyright: ignore[reportCallInDefaultInitializer]
) -> list[CameraSubscriptionSchema]:
    """Gets a list of all camera_subscriptions with pagination."""
    return crud_camera_subscription.get_camera_subscriptions(db_session, skip=page_index * page_size, limit=page_size)


@router.post("/", response_model=CameraSubscription)
def create_camera_subscription(
    camera_subscription: CameraSubscription,
    db_session: Session = Depends(get_db),  # pyright: ignore[reportCallInDefaultInitializer]
) -> CameraSubscriptionSchema:
    """Creates a new camera_subscription with the given details."""
    db_camera_subscription: CameraSubscriptionSchema | None = crud_camera_subscription.get_camera_subscription(
        db_session, camera_subscription
    )

    if db_camera_subscription:
        raise HTTPException(status_code=400, detail="CameraSubscription already exists!")

    db_camera_subscription = crud_camera_subscription.create_camera_subscription(db_session, camera_subscription)
    return db_camera_subscription


@router.get("/", response_model=CameraSubscription)
def get_camera_subscriptions_by_user(
    user_id: int,
    db_session: Session = Depends(get_db),  # pyright: ignore[reportCallInDefaultInitializer]
) -> list[CameraSubscriptionSchema]:
    """Returns a camera_subscription's details using a given user ID."""
    db_camera_subscription: list[CameraSubscriptionSchema] = (
        crud_camera_subscription.get_camera_subscriptions_by_user_id(db_session, user_id)
    )

    if not db_camera_subscription:
        raise HTTPException(status_code=404, detail="CameraSubscription not found!")

    return db_camera_subscription


@router.get("/", response_model=CameraSubscription)
def get_camera_subscriptions_by_camera(
    camera_id: int,
    db_session: Session = Depends(get_db),  # pyright: ignore[reportCallInDefaultInitializer]
) -> list[CameraSubscriptionSchema]:
    """Returns a camera_subscription's details using a given user ID."""
    db_camera_subscription: list[CameraSubscriptionSchema] = (
        crud_camera_subscription.get_camera_subscriptions_by_camera_id(db_session, camera_id)
    )

    if not db_camera_subscription:
        raise HTTPException(status_code=404, detail="CameraSubscription not found!")

    return db_camera_subscription


@router.put("/", response_model=CameraSubscription)
def update_camera_subscription(
    user_id: int,
    camera_ids: list[int],
    db_session: Session = Depends(get_db),  # pyright: ignore[reportCallInDefaultInitializer]
) -> list[CameraSubscriptionSchema]:
    """Updates a camera_subscription's details using a given ID."""
    db_camera_subscription: list[CameraSubscriptionSchema] = crud_camera_subscription.update_camera_subscriptions(
        db_session, user_id, camera_ids
    )

    if not db_camera_subscription:
        raise HTTPException(status_code=404, detail="CameraSubscription not found!")

    return db_camera_subscription


@router.delete("/", response_model=CameraSubscription)
def delete_camera_subscription(
    camera_subscription: CameraSubscription,
    db_session: Session = Depends(get_db),  # pyright: ignore[reportCallInDefaultInitializer]
) -> CameraSubscriptionSchema:
    """Deletes a given camera_subscription by ID."""
    db_camera_subscription: CameraSubscriptionSchema | None = crud_camera_subscription.delete_camera_subscription(
        db_session, camera_subscription
    )

    if not db_camera_subscription:
        raise HTTPException(status_code=404, detail="CameraSubscription not found")

    return db_camera_subscription
