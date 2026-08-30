"""Paginated model class that query params inherit."""

from typing import Annotated

from pydantic import BaseModel, Field


class PaginatedParams(BaseModel):
    """Re-usable model for pagination.

    Also includes some validation.
    """

    page_index: Annotated[int, Field(default=0, ge=0)]
    page_size: Annotated[int, Field(default=100, ge=1)]
