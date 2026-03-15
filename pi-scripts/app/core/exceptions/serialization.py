"""Exceptions related to serialization."""

from pathlib import Path


class SerializationError(Exception):
    """Serialization error."""

    def __init__(self, file_path: Path | str) -> None:
        """Custom constructor for the SerializationError class."""
        super().__init__(f"Failed to serialize {file_path}")
        self.file_path: Path = Path(file_path)
