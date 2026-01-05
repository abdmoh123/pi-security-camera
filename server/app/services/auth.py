"""Module containing CRUD functions related to authentication and token management."""

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.api.auth import create_access_token
from app.api.models.auth import TokenHeader, TokenPayload, TokenPayloadCreate
from app.core.auth.jwt import encode_token
from app.core.config import settings
from app.db.db_models import RefreshToken


def create_refresh_token(db: Session, user_id: int, expires_at: datetime | None = None) -> RefreshToken:
    """Creates and stores a new refresh token for a user.

    The expiry datetime can be defined in advance to allow rotation of refresh tokens.
    """
    # Allows rotation of refresh tokens (better security)
    if expires_at is None:
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    # Generate a random string for the refresh token, or a JWT for specific needs
    # For simplicity, let's generate a JWT for the refresh token as well
    issued_at = datetime.now(timezone.utc)
    refresh_token = encode_token(
        TokenHeader(alg=settings.ALGORITHM),
        TokenPayload(sub=str(user_id), exp=expires_at, iat=issued_at),
        secret=settings.SECRET_KEY,
    )

    db_refresh_token = RefreshToken(token=refresh_token, user_id=user_id, expires_at=expires_at, issued_at=issued_at)
    db.add(db_refresh_token)
    db.commit()
    db.refresh(db_refresh_token)
    return db_refresh_token


def get_refresh_token(db: Session, token: str) -> RefreshToken | None:
    """Retrieves a refresh token from the database."""
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()


def revoke_refresh_token(db: Session, refresh_token: RefreshToken) -> RefreshToken:
    """Revokes a single refresh token by deleting it from the database."""
    db.delete(refresh_token)
    db.commit()
    return refresh_token


def revoke_all_user_refresh_tokens(db: Session, user_id: int) -> list[RefreshToken]:
    """Revokes all refresh tokens for a given user."""
    refresh_tokens = db.query(RefreshToken).filter(RefreshToken.user_id == user_id).all()
    for token in refresh_tokens:
        db.delete(token)
    db.commit()
    return refresh_tokens


def create_personal_access_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    """Creates a long-lived or permanent personal access token (PAT)."""
    # PATs are essentially long-lived access tokens. No refresh token associated.
    # The expiration is handled directly in the JWT.
    return create_access_token(payload=TokenPayloadCreate(sub=str(user_id)), expires_delta=expires_delta)
