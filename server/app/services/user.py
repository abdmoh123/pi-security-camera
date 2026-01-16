"""File containing crud functions related to the User table."""

from argon2 import PasswordHasher
from sqlalchemy.orm import Session

from app.api.models.users import UserCreate, UserUpdate
from app.core.config import settings
from app.core.security.hashing import generate_hashed_password
from app.db.db_models import User


def get_user(db: Session, user_id_or_email: int | str) -> User | None:
    """Automatically chooses between getting a user by ID or email."""
    if isinstance(user_id_or_email, int):
        return get_user_by_id(db, user_id_or_email)
    else:
        return get_user_by_email(db, user_id_or_email)


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Queries the database to get a user using the given ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Queries the database to get a user using the given email address."""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, user_ids: list[int] | None = None, skip: int = 0, limit: int = 100) -> list[User]:
    """Queries and returns a list of all users with pagination.

    If a list of IDs/emails were given, it will only return the given users (if they were found).
    Otherwise, it returns all users in the database (with pagination of course).
    """
    # Just show all users if the id/emails list is None or empty
    if not user_ids:
        return db.query(User).offset(skip).limit(limit).all()

    return db.query(User).filter(User.id.in_(user_ids)).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Creates a new user using the given inputs.

    The first registered user will automatically be made an admin if `ENABLE_FIRST_USER_ADMIN` env variable is True.
    """
    is_first_user = db.query(User).count() == 0
    is_admin = is_first_user and settings.ENABLE_FIRST_USER_ADMIN

    db_user = User(
        email=user.email, password_hash=generate_hashed_password(user.password, PasswordHasher()), is_admin=is_admin
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate) -> User | None:
    """Modifies a given user's parameters (excluding ID) via a given ID or email."""
    db_user: User | None = get_user(db, user_id)

    # skip modifying the database if inputs are empty or if user doesn't exist
    if not user.model_fields_set or not db_user:
        return db_user

    user_as_dict = user.model_dump(exclude_unset=True)
    if user.password:
        user_as_dict["password_hash"] = generate_hashed_password(user.password, PasswordHasher())

    for key, value in user_as_dict.items():  # pyright: ignore[reportAny]
        if key == "password":  # skip password key as it doesn't exist in User table (uses password_hash instead)
            continue
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int) -> User | None:
    """Deletes a given user via ID or email."""
    db_user: User | None = get_user(db, user_id)

    if db_user:
        db.delete(db_user)
        db.commit()

    return db_user
