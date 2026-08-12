"""File containing crud functions related to handling camera subscriptions."""

from sqlalchemy.orm import Session

from pisec_server.api.models.camera_subscriptions import CameraSubscription
from pisec_server.core.exceptions import RecordAlreadyExistsError, RecordNotFoundError
from pisec_server.db.db_models import Camera, User
from pisec_server.services.camera import get_camera, get_cameras
from pisec_server.services.user import get_user, get_users


def get_camera_subscriptions_by_user(db: Session, user_id: int) -> list[CameraSubscription]:
    """Gets all camera subscriptions of the given user."""
    db_user: User | None = get_user(db, user_id)
    if not db_user:
        raise RecordNotFoundError(f"User {user_id} does not exist!")

    # NOTE: Number of subscriptions could be empty
    subscriptions: list[CameraSubscription] = list()
    for camera in db_user.cameras:
        subscriptions.append(CameraSubscription(user_id=db_user.id, camera_id=camera.id))

    return subscriptions


def get_camera_subscriptions_by_camera(db: Session, camera_id: int) -> list[CameraSubscription]:
    """Returns all subscriptions a given camera is assigned to."""
    db_camera: Camera | None = get_camera(db, camera_id)
    if not db_camera:
        raise RecordNotFoundError(f"Camera {camera_id} does not exist!")

    # NOTE: Number of subscriptions could be empty
    subscriptions: list[CameraSubscription] = list()
    for user in db_camera.users:
        subscriptions.append(CameraSubscription(user_id=user.id, camera_id=camera_id))

    return subscriptions


def create_camera_subscriptions_by_user(db: Session, user_id: int, camera_ids: list[int]) -> list[CameraSubscription]:
    """Subscribes the given user to the given cameras."""
    db_user: User | None = get_user(db, user_id)
    # Don't bother subscribing if the user doesn't exist
    if not db_user:
        raise RecordNotFoundError(f"User {user_id} does not exist!")

    # Separate out the cameras that the user is already subscribed to
    current_subscription_ids: list[int] = [sub.camera_id for sub in get_camera_subscriptions_by_user(db, user_id)]
    real_cameras: list[Camera] = get_cameras(db, camera_ids)
    unsubscribed_cameras: list[Camera] = [
        camera for camera in real_cameras if camera.id not in current_subscription_ids
    ]

    if not unsubscribed_cameras:
        raise RecordAlreadyExistsError(f"User {user_id} is already subscribed to all given cameras!")

    # Add the new camera subscriptions
    result: list[CameraSubscription] = list()
    for camera in unsubscribed_cameras:
        db_user.cameras.append(camera)
        result.append(CameraSubscription(user_id=db_user.id, camera_id=camera.id))

    db.commit()

    return result


def create_camera_subscriptions_by_camera(db: Session, camera_id: int, user_ids: list[int]) -> list[CameraSubscription]:
    """Subscribes users to the given camera."""
    db_camera: Camera | None = get_camera(db, camera_id)
    # Don't bother subscribing if the user doesn't exist
    if not db_camera:
        raise RecordNotFoundError(f"Camera {camera_id} does not exist!")

    # Separate out the cameras that the user is already subscribed to
    current_subscription_ids: list[int] = [sub.user_id for sub in get_camera_subscriptions_by_camera(db, camera_id)]
    real_users: list[User] = get_users(db, user_ids)
    unsubscribed_users: list[User] = [user for user in real_users if user.id not in current_subscription_ids]

    if not unsubscribed_users:
        raise RecordAlreadyExistsError(f"Camera {camera_id} is already subscribed to all given users!")

    # Add the new camera subscriptions
    result: list[CameraSubscription] = list()
    for user in unsubscribed_users:
        db_camera.users.append(user)
        result.append(CameraSubscription(user_id=user.id, camera_id=camera_id))

    db.commit()

    return result


def delete_camera_subscriptions_by_user(db: Session, user_id: int, camera_ids: list[int]) -> list[CameraSubscription]:
    """Unsubscribes the user from a given list of cameras."""
    db_user: User | None = get_user(db, user_id)
    # Don't bother subscribing if the user doesn't exist
    if not db_user:
        raise RecordNotFoundError(f"User {user_id} does not exist!")

    # Unlink the cameras from the user
    # NOTE: This will silently skip cameras that aren't already linked
    cameras: list[Camera] = [camera for camera in get_cameras(db, camera_ids) if camera not in db_user.cameras]
    result: list[CameraSubscription] = list()
    for camera in cameras:
        db_user.cameras.remove(camera)
        result.append(CameraSubscription(user_id=db_user.id, camera_id=camera.id))

    db.commit()

    return result


def delete_camera_subscriptions_by_camera(db: Session, camera_id: int, user_ids: list[int]) -> list[CameraSubscription]:
    """Unsubscribes the given users from the given camera."""
    db_camera: Camera | None = get_camera(db, camera_id)
    # Don't bother subscribing if the user doesn't exist
    if not db_camera:
        raise RecordNotFoundError(f"Camera {camera_id} does not exist!")

    # Unlink the cameras from the user
    # NOTE: This will silently skip cameras that aren't already linked
    users: list[User] = [user for user in get_users(db, user_ids) if user not in db_camera.users]
    result: list[CameraSubscription] = list()
    for user in users:
        db_camera.users.remove(user)
        result.append(CameraSubscription(user_id=camera_id, camera_id=user.id))

    db.commit()

    return result
