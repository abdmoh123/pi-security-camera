"""Module containing functions and dependencies for authentication and authorization."""

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
from sqlalchemy.orm import Session

from app.api.models.auth import TokenHeader, TokenPayload, TokenPayloadCreate
from app.core.auth.jwt import decode_token, encode_token
from app.core.config import settings
from app.db.database import get_db
from app.db.db_models import User
from app.services.user import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v0/auth/token")


def create_access_token(payload: TokenPayloadCreate, expires_delta: timedelta | None = None) -> str:
    """Creates a new JWT access token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = TokenPayload(sub=payload.sub, exp=expire, iat=datetime.now(timezone.utc))
    try:
        return encode_token(TokenHeader(alg=settings.ALGORITHM), to_encode)
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not create access token") from e


def decode_access_token(token: str) -> TokenPayload:
    """Decodes a JWT access token and returns its payload."""
    try:
        return decode_token(token)
    except (JWTError, ExpiredSignatureError, JWTClaimsError) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials") from e


async def get_current_user(
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


async def get_current_admin_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """Dependency to get the current authenticated admin user."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user
