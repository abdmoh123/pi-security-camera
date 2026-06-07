"""Pydantic model for a credential token."""


from typing import Literal
from pydantic import BaseModel, Field


class CrendentialToken(BaseModel):
    """Pydantic model for a credential token (JWT).

    Attributes:
        access_token: The JWT access token value
        token_type: The token type (always 'bearer')
    """

    access_token: str = Field(min_length=1)
    token_type: Literal["bearer"]
