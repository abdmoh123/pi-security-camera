"""Reads data from a given data folder."""

from dataclasses import dataclass
from pathlib import Path

from app.core.models.credential import Credential


@dataclass(frozen=True)
class DataReader:
    """Reads data from a given data folder.

    Attributes:
        data_directory: The directory to read data from.
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

    def read_credentials(self) -> Credential:
        """Read the camera credentials from the data directory.

        Returns:
            The camera credentials.
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
        """
        if not self.server_address_path.exists():
            raise FileNotFoundError(
                f"Server address file not found at {self.server_address_path}"
            )

        raw_address = self.server_address_path.read_text().strip()
        # TODO: Do some validation for the address
        return raw_address


def prepare_data_reader(data_directory: Path) -> None:
    """Does some preparation for the DataReader."""
    data_directory.resolve().mkdir(parents=True, exist_ok=True)


def setup_data_reader(data_directory: Path) -> DataReader:
    """Creates a DataReader after doing some preparation and input validation.

    Args:
        data_directory: The directory to read data from.

    Returns:
        The DataReader.
    """
    resolved_data_directory = data_directory.resolve()
    prepare_data_reader(resolved_data_directory)
    return DataReader(resolved_data_directory)
