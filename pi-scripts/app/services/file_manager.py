"""Manages the video files."""


from dataclasses import dataclass
from pathlib import Path

from cv2.typing import MatLike

from app.core.serializers.serializer import Serializer


@dataclass
class FileManager:
    """Manages the video files directory."""

    directory: Path
    max_files: int

    def save_data(
        self,
        data: list[MatLike],
        file_name: str,
        serializer: Serializer,
    ) -> None:
        """Saves a file to the directory.

        Also ensures the max number of files is not exceeded.

        Args:
            data: The video or photo data to save.
            file_name: The name of the file to save.
            serializer: The serializer to use to save the file.

        Raises:
            FileExistsError: If the file already exists.
        """
        # Ensure the max number of files is not exceeded
        num_files = len(self.get_files())
        if num_files >= self.max_files:
            self.delete_oldest_file()

        # Ensure no files are overwritten
        file_path = self.directory / file_name
        if file_path.exists():
            raise FileExistsError(file_path)

        serializer.write_video(data, file_path)

    def get_files(self) -> list[Path]:
        """Reads a list of files in the set directory.

        Returns:
            A list of the files in the directory.
        """
        return list(self.directory.iterdir())

    def delete_oldest_file(self) -> None:
        """Deletes the oldest file in the directory."""
        files = list(self.directory.iterdir())
        if len(files) > self.max_files:
            oldest_file = min(files, key=lambda f: f.stat().st_mtime)
            oldest_file.unlink()
