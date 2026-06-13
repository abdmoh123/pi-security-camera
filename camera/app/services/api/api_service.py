"""Service for interacting with the API server."""

from dataclasses import dataclass, field
from pathlib import Path
from types import TracebackType

import httpx
from httpx import Response

from app.core.models.camera import Camera, CameraUpdate
from app.core.models.user import User
from app.services.api.auth import OAuth2Authenticator


@dataclass
class APIService:
    """Service for interacting with the API server.

    Attributes:
        api_url: The URL of the API server.
        authenticator: The authenticator to use to authenticate with the API
            server.
    """

    api_url: str
    authenticator: OAuth2Authenticator
    _client: httpx.Client = field(init=False)

    def __post_init__(self) -> None:
        """Post init constructor for this API service dataclass."""
        self._client = httpx.Client(
            base_url=self.api_url, auth=self.authenticator
        )

    def __enter__(self) -> "APIService":
        """Context manager entry point."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Context manager exit point."""
        self._client.close()

    def get_registered_users(
        self, page_index: int, page_size: int
    ) -> list[User]:
        """Returns a list of users subscribed to this camera.

        Args:
            page_index: The index of the page to get.
            page_size: The number of users to get per page.

        Returns:
            A list of users registered to this camera.
        """
        if self.authenticator.credential.camera_id is None:
            raise ValueError("Camera ID is not set")

        response: Response = self._client.get(
            url=f"/cameras/{self.authenticator.credential.camera_id}/users",
            auth=self.authenticator,
            params={"page_index": page_index, "page_size": page_size},
        ).raise_for_status()
        return [User(**user) for user in response.json()]  # pyright: ignore[reportAny]

    def upload_video(self, video_path: Path) -> None:
        """Uploads a video to the API server.

        Args:
            video_path: The path to the video to upload.
        """
        with open(video_path, "rb") as video_file:
            _ = self._client.post(
                url="/videos/",
                auth=self.authenticator,
                data={"file_name": video_path.name},
                files={"file": (video_path.name, video_file, "video/mp4")},
            ).raise_for_status()

    def register_camera(
        self, host_address: str, name: str, mac_address: str
    ) -> None:
        """Registers the camera with the server.

        Args:
            host_address: The host address of the camera.
            name: The name of the camera.
            mac_address: The MAC address of the camera.
        """
        response = self._client.post(
            url="/cameras/",
            auth=self.authenticator,
            json={
                "host_address": host_address,
                "name": name,
                "mac_address": mac_address,
            },
        ).raise_for_status()
        camera = Camera(**response.json())  # pyright: ignore[reportAny]
        # Update the credential camera ID in case we want to use it later
        self.authenticator.credential.camera_id = camera.id

    def unregister_camera(self, camera_id: int) -> None:
        """Unregisters the camera from the server.

        Args:
            camera_id: The ID of the camera to unregister.
        """
        _ = self._client.delete(
            url=f"/cameras/{camera_id}",
            auth=self.authenticator,
        ).raise_for_status()
        # Reset the credential camera ID back to None
        self.authenticator.credential.camera_id = None

    def update_camera(self, camera_data: CameraUpdate) -> None:
        """Updates the camera's data on the server.

        Args:
            camera_data: The data to update the camera with.
        """
        if self.authenticator.credential.camera_id is None:
            raise ValueError("Camera ID is not set")

        _ = self._client.put(
            url=f"/cameras/{self.authenticator.credential.camera_id}",
            auth=self.authenticator,
            json=camera_data.model_dump(),
        ).raise_for_status()
