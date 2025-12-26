"""This module contains pydantic models for general use cases."""

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Re-usable model for pagination.

    Also includes some validation.
    """

    page_index: int = Field(default=0, ge=0)
    page_size: int = Field(default=100, ge=1)
