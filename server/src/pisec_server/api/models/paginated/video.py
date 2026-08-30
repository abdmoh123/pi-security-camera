"""Query parameters for paginated video responses."""

from typing import Annotated

from fastapi import Query

from pisec_server.api.models.paginated.generic import Paginated
from pisec_server.core.validation.regex import file_name_regex


class VideoGetParams(Paginated):
    """Video GET query parameters with pagination."""

    video_id: Annotated[list[int] | None, Query(ge=1)] = None  # Named in singular form due to how it's queried
    camera_id: Annotated[list[int] | None, Query(ge=1)] = None  # Named in singular form due to how it's queried
    file_name: Annotated[str | None, Query(regex=file_name_regex, min_length=5)] = None
