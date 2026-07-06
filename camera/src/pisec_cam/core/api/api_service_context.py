"""Data to be sent to all APIService objects and stuff related."""

from dataclasses import dataclass

from pisec_cam.services.api.auth import OAuth2Authenticator


@dataclass(frozen=True)
class APIServiceContext:
    """Context for APIService objects.

    Attributes:
        api_url: The URL of the API server.
        authenticator: The authenticator to use to authenticate with the API
            server.
    """

    api_url: str
    authenticator: OAuth2Authenticator
