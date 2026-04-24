"""Exceptions related to serialization."""

from pathlib import Path


class SerializationError(Exception):
    """Custom serialization exception."""

    def __init__(self, file_path: Path | str) -> None:
        """Custom constructor for the SerializationError class.

        The file path can be stored internally to allow for easier and more
        detailed error messages.

        Args:
            file_path: The path to the file that could not be serialized.
        """
        super().__init__(f"Failed to serialize {file_path}")
        self.file_path: Path = Path(file_path)
