"""File containing crud functions related to handling camera subscriptions."""

from sqlalchemy.orm import Session

from app.api.models.camera_subscriptions import CameraSubscription
from app.db.db_models import Camera, User
from app.services.camera import get_camera, get_cameras
from app.services.user import get_user, get_users


def get_camera_subscriptions_by_user(db: Session, user_id: int) -> list[CameraSubscription]:
    """Gets all camera subscriptions of the given user."""
    subscriptions: list[CameraSubscription] = list()

    db_user: User | None = get_user(db, user_id)
    if not db_user:
        return subscriptions

    for camera in db_user.cameras:
        subscriptions.append(CameraSubscription(user_id=db_user.id, camera_id=camera.id))

    return subscriptions


def get_camera_subscriptions_by_camera(db: Session, camera_id: int) -> list[CameraSubscription]:
    """Returns all subscriptions a given camera is assigned to."""
    subscriptions: list[CameraSubscription] = list()

    db_camera: Camera | None = get_camera(db, camera_id)
    if not db_camera:
        return subscriptions

    for user in db_camera.users:
        subscriptions.append(CameraSubscription(user_id=user.id, camera_id=camera_id))

    return subscriptions


def create_camera_subscriptions_by_user(db: Session, user_id: int, camera_ids: list[int]) -> list[CameraSubscription]:
    """Subscribes to given user to the given cameras."""
    db_user: User | None = get_user(db, user_id)
    # don't bother subscribing if the user doesn't exist
    if not db_user:
        return []

    # separate out the cameras that the user is already subscribed to
    current_subscriptions: list[CameraSubscription] = get_camera_subscriptions_by_user(db, user_id)
    subscribed_camera_ids: set[int] = set([sub.camera_id for sub in current_subscriptions])
    unsubscribed_camera_ids: set[int] = set(camera_ids) - subscribed_camera_ids

    # add the new camera subscriptions
    result: list[CameraSubscription] = list()
    for id in unsubscribed_camera_ids:
        camera: Camera | None = get_camera(db, id)
        if camera:
            db_user.cameras.append(camera)
            result.append(CameraSubscription(user_id=db_user.id, camera_id=camera.id))

    db.commit()

    return result


def create_camera_subscriptions_by_camera(db: Session, camera_id: int, user_ids: list[int]) -> list[CameraSubscription]:
    """Subscribes users to the given camera."""
    db_camera: Camera | None = get_camera(db, camera_id)
    # don't bother subscribing if the user doesn't exist
    if not db_camera:
        return []

    # separate out the cameras that the user is already subscribed to
    current_subscriptions: list[CameraSubscription] = get_camera_subscriptions_by_camera(db, camera_id)
    subscribed_user_ids: set[int] = set([sub.user_id for sub in current_subscriptions])
    unsubscribed_user_ids: set[int] = set(user_ids) - subscribed_user_ids

    # add the new camera subscriptions
    result: list[CameraSubscription] = list()
    for id in unsubscribed_user_ids:
        user: User | None = get_user(db, id)
        if user:
            db_camera.users.append(user)
            result.append(CameraSubscription(user_id=user.id, camera_id=camera_id))

    db.commit()

    return result


def delete_camera_subscriptions_by_user(db: Session, user_id: int, camera_ids: list[int]) -> list[CameraSubscription]:
    """Unsubscribes the user from a given list of cameras."""
    db_user: User | None = get_user(db, user_id)
    # don't bother subscribing if the user doesn't exist
    if not db_user:
        return []

    # unlink the cameras from the user
    cameras: list[Camera] = get_cameras(db, camera_ids)
    result: list[CameraSubscription] = list()
    for camera in cameras:
        db_user.cameras.remove(camera)
        result.append(CameraSubscription(user_id=db_user.id, camera_id=camera.id))

    db.commit()

    return result


def delete_camera_subscriptions_by_camera(db: Session, camera_id: int, user_ids: list[int]) -> list[CameraSubscription]:
    """Unsubscribes the given users from the given camera."""
    db_camera: Camera | None = get_camera(db, camera_id)
    # don't bother subscribing if the user doesn't exist
    if not db_camera:
        return []

    # unlink the cameras from the user
    users: list[User] = get_users(db, user_ids)
    result: list[CameraSubscription] = list()
    for user in users:
        db_camera.users.remove(user)
        result.append(CameraSubscription(user_id=camera_id, camera_id=user.id))

    db.commit()

    return result
