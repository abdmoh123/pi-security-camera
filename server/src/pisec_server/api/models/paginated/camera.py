"""Query parameters for paginated camera responses."""

from typing import Annotated

from fastapi import Query

from pisec_server.api.models.paginated.generic import PaginatedParams
from pisec_server.core.validation.regex import camera_name_regex, mac_address_regex


class CameraGetParams(PaginatedParams):
    """Camera GET query parameters with pagination."""

    camera_id: Annotated[list[int] | None, Query(ge=1)] = None  # Named in singular form due to how it's queried
    user_id: Annotated[list[int] | None, Query(ge=1)] = None  # Named in singular form due to how it's queried
    name: Annotated[str | None, Query(regex=camera_name_regex)] = None
    mac_address: Annotated[str | None, Query(regex=mac_address_regex)] = None
