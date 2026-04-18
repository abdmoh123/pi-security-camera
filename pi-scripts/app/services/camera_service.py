"""Camera service containing business logic for running the camera."""

import datetime
from dataclasses import dataclass
from pathlib import Path

# TODO: Remove dependency on opencv for MatLike data structure
from cv2.typing import MatLike

from app.core.cameras.camera import Camera
from app.core.serializers.serializer import Serializer


@dataclass
class CameraService:
    """Camera service containing business logic for running the camera."""

    camera: Camera
    serializer: Serializer
    video_dir: Path
    photo_dir: Path

    def __init__(
        self,
        camera: Camera,
        serializer: Serializer,
        video_dir: Path | None = None,
        photo_dir: Path | None = None,
    ) -> None:
        """Initializes the camera service."""
        self.camera = camera
        self.serializer = serializer

        # Set default directories
        if video_dir is None:
            video_dir = Path("./recordings")
        if photo_dir is None:
            photo_dir = Path("./photos")

        self.video_dir = video_dir
        self.photo_dir = photo_dir

        # Ensure directories exist
        self.video_dir.mkdir(exist_ok=True, parents=True)
        self.photo_dir.mkdir(exist_ok=True, parents=True)

    def record_video(self, seconds: int) -> None:
        """Creates a video recording of the camera."""
        print(f"Recording for {seconds} seconds")
        data: list[MatLike] = self.camera.start_recording(seconds)
        print(f"Recorded {len(data)} frames successfully!")

        current_timestamp: str = datetime.datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )
        filename: str = f"video-{current_timestamp}.mp4"

        print(f"Writing video: {filename}...")
        self.serializer.write_video(data, self.video_dir / filename)
        print("Video written succesfully!")

    def take_photo(self) -> None:
        """Captures a frame from the camera and saves it to a file."""
        print("Taking photo...")
        data: MatLike = self.camera.capture_frame()
        print("Photo taken successfully!")

        current_timestamp: str = datetime.datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )
        filename: str = f"photo-{current_timestamp}.jpg"

        print(f"Saving photo: {filename}...")
        # WARN: Can raise a SerializationError
        self.serializer.write_image(data, self.photo_dir / filename)
        print("Image written successfully!")
