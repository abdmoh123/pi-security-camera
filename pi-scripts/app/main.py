"""Main endpoint of the application."""

import time
from pathlib import Path

import typer

from app.core.cameras.opencv_camera import OpenCVCamera
from app.core.serializers.opencv_serializer import OpenCVSerializer
from app.services.camera_service import CameraService
from app.services.motion.frame_difference_detector import (
    CV2FrameDifferenceDetectorService,
)

app = typer.Typer()


@app.command()
def serve(
    wait_time_ms: int = 1000,
    delta_ms: int = 500,
    video_length_s: int = 10,
    video_dir: str = "./recordings"
) -> None:
    """Runs the motion detection service."""
    with OpenCVCamera() as camera:
        motion_detector = CV2FrameDifferenceDetectorService(camera)
        camera_service = CameraService(
            camera, OpenCVSerializer(), video_dir=Path(video_dir)
        )
        while True:
            print(f"Sleeping for {wait_time_ms // 1000} seconds...")
            time.sleep(wait_time_ms // 1000)
            detected = motion_detector.detect_motion(delta_ms)
            if detected:
                print("Motion detected: Recording video...")
                camera_service.record_video(video_length_s)
            else:
                print("Motion not detected")


@app.command()
def record(seconds: int = 600, video_dir: str = "./recordings") -> None:
    """Starts the camera recording routine."""
    with OpenCVCamera() as camera:
        camera_service = CameraService(
            camera, OpenCVSerializer(), video_dir=Path(video_dir)
        )
        camera_service.record_video(seconds)


@app.command()
def shoot(photo_dir: str = "./photos") -> None:
    """Captures the current frame from the camera."""
    with OpenCVCamera() as camera:
        camera_service = CameraService(
            camera, OpenCVSerializer(), photo_dir=Path(photo_dir)
        )
        camera_service.take_photo()


if __name__ == "__main__":
    app()
