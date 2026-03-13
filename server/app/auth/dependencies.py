"""Module containing functions and dependencies for authentication and authorization."""

from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.services import decode_access_token
from app.db.database import get_db
from app.db.db_models import User
from app.services.user import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v0/auth/token")


def get_current_user(
    db_session: Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    """Dependency to get the current authenticated user."""
    payload = decode_access_token(token)
    # Shouldn't need to check expiry due to ExpiredSignatureError, but kept just in case
    if payload.exp < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")

    try:
        user_id: int = int(payload.sub)
    except ValueError:
        raise ValueError("Token subject isn't valid!")

    user: User | None = get_user(db_session, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    return user


def get_current_admin_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """Dependency to get the current authenticated admin user."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user
