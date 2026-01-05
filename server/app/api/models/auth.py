"""File containing pydantic models for authentication-related data."""

from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    """Pydantic model for returning JWT access tokens."""

    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class TokenHeader(BaseModel):
    """Pydantic model for the header of a access token."""

    alg: str  # Algorithm used (e.g. HS256)
    typ: str = "JWT"  # Type of token (e.g. JWT)


class TokenPayloadCreate(BaseModel):
    """Pydantic model for creating a JWT access token payload."""

    sub: str  # Subject (usually a user ID)


class TokenPayload(TokenPayloadCreate):
    """Pydantic model for the payload of a JWT access token."""

    exp: datetime  # Expiration date + time
    iat: datetime  # Date + time the token was issued at
