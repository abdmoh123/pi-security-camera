"""File containing crud functions related to the CameraCredential table."""

from argon2 import PasswordHasher
from sqlalchemy.orm import Session

from app.api.models.camera_credentials import CameraCredentialCreate
from app.core.exceptions import RecordAlreadyExistsError, RecordNotFoundError
from app.core.security.hashing import generate_hashed_password
from app.db.db_models import Camera, CameraCredential
from app.services.camera import get_camera


# TODO: Use sqlalchemy select instead of query
def get_credential(db: Session, client_id: str) -> CameraCredential | None:
    """Queries the database to get a camera credential using the given ID."""
    return db.query(CameraCredential).filter(CameraCredential.client_id == client_id).first()


def create_credential(db: Session, credential: CameraCredentialCreate) -> CameraCredential:
    """Creates a new camera credential using the given inputs."""
    db_credential: CameraCredential | None = get_credential(db, credential.client_id)
    if db_credential:
        raise RecordAlreadyExistsError(f"Camera credential with client ID {credential.client_id} already exists!")

    db_credential = CameraCredential(
        client_id=credential.client_id,
        client_secret_hash=generate_hashed_password(credential.client_secret, PasswordHasher()),
    )
    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)

    return db_credential


def assign_camera(db: Session, client_id: str, camera_id: int) -> CameraCredential | None:
    """Assigns a camera to a given camera credential.

    NOTE: This function will not create a Camera record if it does not exist.
    """
    db_credential: CameraCredential | None = get_credential(db, client_id)
    if not db_credential:
        raise RecordNotFoundError(f"Camera credential {client_id} does not exist!")

    # Camera should be created before assigning to a credential via the camera service
    db_camera: Camera | None = get_camera(db, camera_id)
    if not db_camera:
        raise RecordNotFoundError(f"Camera {camera_id} does not exist!")

    db_credential.camera_id = camera_id
    db.commit()
    db.refresh(db_credential)

    return db_credential


def delete_credential(db: Session, client_id: str) -> CameraCredential | None:
    """Deletes a given camera credential by ID."""
    db_credential: CameraCredential | None = get_credential(db, client_id)

    if not db_credential:
        raise RecordNotFoundError(f"Camera credential {client_id} does not exist!")

    db.delete(db_credential)
    db.commit()

    return db_credential
