"""Camera service containing business logic for running the camera."""

from dataclasses import dataclass

# TODO: Remove dependency on opencv for MatLike data structure
from cv2.typing import MatLike

from app.core.cameras.camera import Camera
from app.core.serializers.serializer import Serializer
from app.services.file_manager import FileManager
from app.services.file_name_generator import (
    generate_timestamp_photo_name,
    generate_timestamp_video_name,
)


@dataclass(frozen=True)
class CameraService:
    """Camera service containing business logic for running the camera.

    Attributes:
        camera: The camera to use.
        serializer: The serializer to use.
        file_manager: The file manager to use.
    """

    camera: Camera
    serializer: Serializer
    file_manager: FileManager

    def record_video(self, seconds: int) -> None:
        """Creates a video recording of the camera.

        Args:
            seconds: The number of seconds to record.
        """
        print(f"Recording for {seconds} seconds")
        data: list[MatLike] = self.camera.start_recording(seconds)
        print(f"Recorded {len(data)} frames successfully!")

        print(f"Saving video: {generate_timestamp_video_name()}...")
        self.file_manager.save_data(
            data, generate_timestamp_video_name, self.serializer
        )
        print("Video saved succesfully!")

    def take_photo(self) -> None:
        """Captures a frame from the camera and saves it to a file."""
        print("Taking photo...")
        data: MatLike = self.camera.capture_frame()
        print("Photo taken successfully!")

        print(f"Saving photo: {generate_timestamp_photo_name()}...")
        self.file_manager.save_data(
            data, generate_timestamp_photo_name, self.serializer
        )
        print("Image saved successfully!")
