"""Functions related to handling jwts."""

from jose import jwt

from app.api.models.auth import TokenHeader, TokenPayload
from app.core.config import settings


def encode_token(header: TokenHeader, payload: TokenPayload, secret: str = settings.SECRET_KEY) -> str:
    """Encodes a token payload into a JWT using pydantic models."""
    return jwt.encode(claims=payload.model_dump(), key=secret, algorithm=header.alg, headers=header.model_dump())


def decode_token(token: str, secret: str = settings.SECRET_KEY, algorithm: str = settings.ALGORITHM) -> TokenPayload:
    """Decodes a jwt to a pydantic model of a token payload."""
    payload = jwt.decode(token, secret, algorithms=[algorithm])
    return TokenPayload(sub=payload["sub"], exp=payload["exp"], iat=payload["iat"])  # pyright: ignore[reportAny]
