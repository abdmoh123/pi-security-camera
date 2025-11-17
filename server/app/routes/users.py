"""FastAPI routes related to the Camera table."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api_schemas import UserCreate, UserUpdate, User
from app.database import get_db
from app.crud import user as crud_user
from app.db_models import User as UserSchema


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[User])
def get_users(page_index: int = 0, page_size: int = 100, db_session: Session = Depends(get_db)) -> list[UserSchema]:  # pyright: ignore[reportCallInDefaultInitializer]
    """Gets a list of all users with pagination."""
    return crud_user.get_users(db_session, skip=page_index * page_size, limit=page_size)


@router.post("/", response_model=User)
def create_user(user: UserCreate, db_session: Session = Depends(get_db)) -> UserSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Creates a new user with the given details."""
    db_user: UserSchema | None = crud_user.get_user_by_email(db_session, user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="User already exists!")

    db_user = crud_user.create_user(db_session, user)
    return db_user


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db_session: Session = Depends(get_db)) -> UserSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Returns a user's details using a given ID."""
    db_user: UserSchema | None = crud_user.get_user(db_session, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    return db_user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db_session: Session = Depends(get_db)) -> UserSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Updates a user's details using a given ID."""
    db_user: UserSchema | None = crud_user.update_user(db_session, user_id, user)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")

    return db_user


@router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int, db_session: Session = Depends(get_db)) -> UserSchema:  # pyright: ignore[reportCallInDefaultInitializer]
    """Deletes a given user by ID."""
    db_user: UserSchema | None = crud_user.delete_user(db_session, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user
