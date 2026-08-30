"""Query parameters for paginated user responses."""

from typing import Annotated

from fastapi import Query

from pisec_server.api.models.paginated.generic import PaginatedParams


class UserGetParams(PaginatedParams):
    """User GET query parameters with pagination."""

    user_id: Annotated[list[int] | None, Query()] = None  # Named in singular form due to how it's queried
    camera_id: Annotated[list[int] | None, Query()] = None  # Named in singular form due to how it's queried
    email: Annotated[str | None, Query()] = None
