"""Main endpoint of the application."""

from pathlib import Path

import typer

from app.core.cameras.opencv_camera import OpenCVCamera
from app.core.serializers.opencv_serializer import OpenCVSerializer
from app.services.camera_service import CameraService

app = typer.Typer()


@app.command()
def record(seconds: int = 600, video_dir: str = "./recordings") -> None:
    """Starts the camera recording routine."""
    with CameraService(
        OpenCVCamera(), OpenCVSerializer(), video_dir=Path(video_dir)
    ) as camera_service:
        camera_service.record_video(seconds)


@app.command()
def shoot(photo_dir: str = "./photos") -> None:
    """Captures the current frame from the camera."""
    with CameraService(
        OpenCVCamera(), OpenCVSerializer(), photo_dir=Path(photo_dir)
    ) as camera_service:
        camera_service.take_photo()


if __name__ == "__main__":
    app()
