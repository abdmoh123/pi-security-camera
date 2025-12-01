"""File containing crud functions related to the User table."""

from sqlalchemy.orm import Session

from app.api_schemas import UserCreate, UserUpdate
from app.db_models import User


def get_user(db: Session, user_id: int) -> User | None:
    """Queries the database to get a user using the given ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Queries the database to get a user using the given email address."""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, user_ids: list[int] | None = None, skip: int = 0, limit: int = 100) -> list[User]:
    """Queries and returns a list of all users with pagination.

    If a list of IDs were given, it will only return the given users (if they were found).
    Otherwise, it returns all users in the database (with pagination of course).
    """
    if not user_ids:
        return db.query(User).offset(skip).limit(limit).all()
    return db.query(User).filter(User.id.in_(user_ids)).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Creates a new user using the given inputs."""
    db_user = User(email=user.email, password_hash=user.password_hash)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate) -> User | None:
    """Modifies a given user's parameters (excluding ID) via a given ID."""
    db_user = db.query(User).filter(User.id == user_id).first()

    # skip modifying the database if inputs are empty or if user doesn't exist
    if not user.model_fields_set or not db_user:
        return db_user

    user_as_dict = user.model_dump(exclude_unset=True)

    for key, value in user_as_dict.items():  # pyright: ignore[reportAny]
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int) -> User | None:
    """Deletes a given user via ID."""
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user:
        db.delete(db_user)
        db.commit()

    return db_user
