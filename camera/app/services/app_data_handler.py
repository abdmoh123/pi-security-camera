"""Reads data from a given data folder."""

import re
from dataclasses import dataclass
from pathlib import Path

from app.config import settings
from app.core.models.camera import BaseCamera
from app.core.models.credential import Credential


@dataclass(frozen=True)
class AppDataHandler:
    """Handles reading and writing data in the app's data directory.

    The path is customisable and given via the constructor.

    Attributes:
        data_directory: The data directory to read and write data.
    """

    data_directory: Path

    def __post_init__(self) -> None:
        """Perform some validation on the DataReader attributes."""
        if not self.data_directory.exists():
            raise FileNotFoundError(
                f"Data directory not found at {self.data_directory}"
            )

    @property
    def server_address_path(self) -> Path:
        """Property for the path to the file containing the API server address.

        Returns:
            The path to the API server address file.
        """
        return self.data_directory / "server_address.txt"

    @property
    def credentials_path(self) -> Path:
        """Property for the path to the credentials file.

        Returns:
            The path to the credentials file.
        """
        return self.data_directory / "credentials.json"

    @property
    def camera_details_path(self) -> Path:
        """Property for the path to the camera details file.

        Returns:
            The path to the camera details file.
        """
        return self.data_directory / "camera_details.json"

    def read_credentials(self) -> Credential:
        """Read the camera credentials from the data directory.

        Returns:
            The camera credentials.

        Raises:
            FileNotFoundError: If the credentials file is not found.
        """
        if not self.credentials_path.exists():
            raise FileNotFoundError(
                f"Credentials file not found at {self.credentials_path}"
            )

        return Credential.model_validate_json(self.credentials_path.read_text())

    def update_credentials_file(self, new_credentials: Credential) -> None:
        """Update the credentials file with new credentials.

        Args:
            new_credentials: The new credentials.
        """
        _ = self.credentials_path.write_text(new_credentials.model_dump_json())

    def read_server_address(self) -> str:
        """Read the API server address from the data directory.

        Returns:
            The server host.

        Raises:
            FileNotFoundError: If the server address file is not found.
        """
        if not self.server_address_path.exists():
            raise FileNotFoundError(
                f"Server address file not found at {self.server_address_path}"
            )

        raw_address: str = self.server_address_path.read_text().strip()
        pattern = r"^https?://.*"
        if "\n" in raw_address or re.match(pattern, raw_address) is None:
            raise ValueError(f"Invalid server address: {raw_address}")

        return raw_address

    def read_camera_details(self) -> BaseCamera:
        """Read the camera details from the data directory.

        Returns:
            The camera details pydantic model.

        Raises:
            FileNotFoundError: If the camera details file is not found.
        """
        if not self.camera_details_path.exists():
            raise FileNotFoundError(
                f"Camera details file not found at {self.camera_details_path}"
            )

        return BaseCamera.model_validate_json(
            self.camera_details_path.read_text()
        )


def prepare_data_reader(data_directory: Path) -> None:
    """Does some preparation for the AppDataHandler.

    Args:
        data_directory: The directory to read data from.
    """
    data_directory.resolve().mkdir(parents=True, exist_ok=True)


def setup_data_reader(data_directory: Path) -> AppDataHandler:
    """Creates a AppDataHandler after doing some validation.

    Args:
        data_directory: The directory to read data from.

    Returns:
        The AppDataHandler.
    """
    resolved_data_directory = data_directory.resolve()
    prepare_data_reader(resolved_data_directory)
    return AppDataHandler(resolved_data_directory)


app_data_handler = setup_data_reader(settings.data_dir)
