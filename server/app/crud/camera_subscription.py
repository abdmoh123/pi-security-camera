"""File containing crud functions related to the CameraSubscription table."""

from sqlalchemy.orm import Session
from app.db_models import CameraSubscription
from app.api_schemas import CameraSubscription as CameraSubscriptionModel


def get_camera_subscription(db: Session, camera_subscription: CameraSubscriptionModel) -> CameraSubscription | None:
    """Queries the database to get a camera_subscription using the given user and camera IDs.

    Only useful for checking if a subscription exists.
    """
    return (
        db.query(CameraSubscription)
        .filter(
            CameraSubscription.user_id == camera_subscription.user_id,
            CameraSubscription.camera_id == camera_subscription.camera_id,
        )
        .first()
    )


def get_camera_subscriptions(db: Session, skip: int = 0, limit: int = 100) -> list[CameraSubscription]:
    """Queries and returns a list of all camera_subscriptions with pagination."""
    return db.query(CameraSubscription).offset(skip).limit(limit).all()


def get_camera_subscriptions_by_user_id(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> list[CameraSubscription]:
    """Returns all of a given user's camera subscriptions."""
    return db.query(CameraSubscription).filter(CameraSubscription.user_id == user_id).offset(skip).limit(limit).all()


def get_camera_subscriptions_by_camera_id(
    db: Session, camera_id: int, skip: int = 0, limit: int = 100
) -> list[CameraSubscription]:
    """Returns all subscriptions a given camera is assigned to."""
    return (
        db.query(CameraSubscription).filter(CameraSubscription.camera_id == camera_id).offset(skip).limit(limit).all()
    )


def create_camera_subscription(db: Session, camera_subscription: CameraSubscriptionModel) -> CameraSubscription:
    """Creates a new camera_subscription using the given inputs."""
    db_camera_subscription = CameraSubscription(
        user_id=camera_subscription.user_id,
        camera_id=camera_subscription.camera_id,
    )

    db.add(db_camera_subscription)
    db.commit()
    db.refresh(db_camera_subscription)

    return db_camera_subscription


def update_camera_subscriptions(db: Session, user_id: int, camera_ids: list[int]) -> list[CameraSubscription]:
    """Replaces a user's camera subscriptions.

    After running this query, the given user should only be subscribed to the given cameras.
    If the camera ID list is empty, then this should unsubscribe the user from all cameras.
    """
    old_subscriptions: list[CameraSubscription] = get_camera_subscriptions_by_user_id(db, user_id)

    # find which subscriptions already exist (skip redundant database queries) and which ones need to be created
    subscriptions_to_keep: list[CameraSubscriptionModel] = list()
    subscriptions_to_create: list[CameraSubscriptionModel] = list()
    for camera_id in camera_ids:
        already_exists: bool = False
        for subscription in old_subscriptions:
            if subscription.camera_id == camera_id:
                already_exists = True
                subscription_model = CameraSubscriptionModel(
                    user_id=subscription.user_id, camera_id=subscription.camera_id
                )
                if subscription_model not in subscriptions_to_keep:
                    subscriptions_to_keep.append(subscription_model)
                break
        if not already_exists:
            subscriptions_to_create.append(CameraSubscriptionModel(user_id=user_id, camera_id=camera_id))

    # delete all the extra subscriptions that weren't specified in the list of camera IDs
    deleted_subscriptions: list[CameraSubscription] = list()
    for subscription in old_subscriptions:
        subscription_model = CameraSubscriptionModel(user_id=subscription.user_id, camera_id=subscription.camera_id)
        if subscription_model not in subscriptions_to_keep and subscription_model not in subscriptions_to_create:
            res: CameraSubscription | None = delete_camera_subscription(db, subscription_model)
            if res is not None:
                deleted_subscriptions.append(res)

    # should return both the created and deleted camera subscriptions
    result: list[CameraSubscription] = [create_camera_subscription(db, sub) for sub in subscriptions_to_create]
    result.extend(deleted_subscriptions)
    return result


def delete_camera_subscription(db: Session, camera_subscription: CameraSubscriptionModel) -> CameraSubscription | None:
    """Deletes a given camera_subscription via ID."""
    db_camera_subscription = (
        db.query(CameraSubscription)
        .filter(
            CameraSubscription.user_id == camera_subscription.user_id,
            CameraSubscription.camera_id == camera_subscription.camera_id,
        )
        .first()
    )

    if db_camera_subscription:
        db.delete(db_camera_subscription)
        db.commit()

    return db_camera_subscription
