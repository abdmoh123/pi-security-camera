"""Manages the video files."""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from cv2.typing import MatLike

from app.core.serializers.serializer import Serializer


@dataclass(frozen=True)
class FileManager:
    """Manages the video files directory."""

    directory: Path
    max_files: int

    def __is_full(self, num_files: int) -> bool:
        """Checks if the directory is full [private function].

        Setting a negative number will disable this check.

        Args:
            num_files: The number of files in the directory.

        Returns:
            True if the directory is full, False otherwise.
        """
        return self.max_files > 0 and num_files >= self.max_files

    def save_data(
        self,
        data: list[MatLike] | MatLike,
        file_name_generator: Callable[[], str],
        serializer: Serializer,
    ) -> None:
        """Saves a video or image to the directory.

        Also ensures the max number of files is not exceeded.

        Args:
            data: The video or image data to save.
            file_name_generator: Function to generate the file name.
            serializer: The serializer to use to save the file.

        Raises:
            FileExistsError: If the file already exists.
        """
        # Ensure the max number of files is not exceeded
        num_files = len(self.get_files())
        while self.__is_full(num_files):
            self.delete_oldest_file()

        # Ensure no files are overwritten
        file_path = self.directory / file_name_generator()
        if file_path.exists():
            raise FileExistsError(file_path)

        # Save the data as a video or image accordingly
        if isinstance(data, list):
            serializer.write_video(data, file_path)
        else:
            serializer.write_image(data, file_path)

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
