"""Main endpoint of the application."""

import time
from pathlib import Path

import typer

from app.core.cameras.opencv_camera import OpenCVCamera
from app.core.serializers.opencv_serializer import OpenCVSerializer
from app.services.camera_service import CameraService
from app.services.file_manager import FileManager
from app.services.motion.frame_difference_detector import (
    CV2FrameDifferenceDetectorService,
)

app = typer.Typer()


@app.command()
def serve(
    wait_time_ms: int = 1000,
    delta_ms: int = 500,
    video_length_s: int = 10,
    video_dir: str = "./recordings",
    max_files: int = 5,
) -> None:
    """Runs the motion detection service.

    Args:
        wait_time_ms: The number of milliseconds to sleep between checks.
            Defaults to 1000ms (1s).
        delta_ms: The number of milliseconds to wait between frames.
            Defaults to 500ms (0.5s).
        video_length_s: The number of seconds to record a video.
            Defaults to 10s.
        video_dir: The directory (string) to save the video to.
            Defaults to "./recordings".
        max_files: The maximum number of files to keep in the directory.
            Defaults to 5 files.
    """
    with OpenCVCamera() as camera:
        motion_detector = CV2FrameDifferenceDetectorService(camera)
        file_manager = FileManager(Path(video_dir), max_files)
        serializer = OpenCVSerializer()
        camera_service = CameraService(camera, serializer, file_manager)
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
    """Starts the camera recording routine.

    Args:
        seconds: The number of seconds to record.
            Defaults to 600s (10mins).
        video_dir: The directory (string) to save the video to.
            Defaults to "./recordings".
    """
    with OpenCVCamera() as camera:
        # Negative max_files disables the check
        file_manager = FileManager(Path(video_dir), max_files=-1)
        serializer = OpenCVSerializer()
        camera_service = CameraService(camera, serializer, file_manager)
        camera_service.record_video(seconds)


@app.command()
def shoot(photo_dir: str = "./photos") -> None:
    """Captures the current frame from the camera.

    Args:
        photo_dir: The directory (string) to save the photo to.
            Defaults to "./photos".
    """
    with OpenCVCamera() as camera:
        # Negative max_files disables the check
        file_manager = FileManager(Path(photo_dir), max_files=-1)
        serializer = OpenCVSerializer()
        camera_service = CameraService(camera, serializer, file_manager)
        camera_service.take_photo()


if __name__ == "__main__":
    app()
