"""Camera service containing business logic for running the camera."""

from dataclasses import dataclass
from pathlib import Path

# TODO: Remove dependency on opencv for MatLike data structure
from cv2.typing import MatLike

from app.core.cameras.camera import Camera
from app.core.serializers.serializer import Serializer
from app.services.file_manager import FileManager
from app.services.file_name_generator import (
    generate_timestamp_photo_name,
    generate_timestamp_video_name,
)


@dataclass
class CameraService:
    """Camera service containing business logic for running the camera."""

    camera: Camera
    serializer: Serializer
    file_manager: FileManager
    photo_dir: Path

    def __init__(
        self,
        camera: Camera,
        serializer: Serializer,
        file_manager: FileManager,
    ) -> None:
        """Initializes the camera service."""
        self.camera = camera
        self.serializer = serializer
        self.file_manager = file_manager

    def record_video(self, seconds: int) -> None:
        """Creates a video recording of the camera."""
        print(f"Recording for {seconds} seconds")
        data: list[MatLike] = self.camera.start_recording(seconds)
        print(f"Recorded {len(data)} frames successfully!")

        def filename_func() -> str:
            return generate_timestamp_video_name("mp4")

        print(f"Writing video: {filename_func()}...")
        self.file_manager.save_data(data, filename_func, self.serializer)
        print("Video written succesfully!")

    def take_photo(self) -> None:
        """Captures a frame from the camera and saves it to a file."""
        print("Taking photo...")
        data: MatLike = self.camera.capture_frame()
        print("Photo taken successfully!")

        def filename_func() -> str:
            return generate_timestamp_photo_name("jpg")

        print(f"Saving photo: {filename_func()}...")
        # WARN: Can raise a SerializationError
        self.file_manager.save_data(data, filename_func, self.serializer)
        print("Image written successfully!")
