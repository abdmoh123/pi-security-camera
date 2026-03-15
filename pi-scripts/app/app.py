"""Main endpoint of the application."""

import datetime
from pathlib import Path

import cv2
import typer

from app.core.cameras.opencv_camera import OpenCVCamera

app = typer.Typer()


@app.command()
def record(seconds: int = 600, video_dir: str = "./recordings") -> None:
    """Starts the camera recording routine."""
    print(f"Recording for {seconds} seconds")
    with OpenCVCamera() as camera:
        data = camera.start_recording(seconds)
    print(f"Recorded {len(data)} frames")

    video_dir_path: Path = Path(video_dir)
    video_dir_path.mkdir(exist_ok=True, parents=True)

    current_timestamp: str = datetime.datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    filename: str = f"video-{current_timestamp}.mp4"
    print(f"Saving file: {filename}...")

    print("Writing video...")
    out = cv2.VideoWriter(
        filename=video_dir_path / filename,
        fourcc=cv2.VideoWriter_fourcc(*"mp4v"),
        fps=24.0,
        frameSize=data[0].shape[1::-1],
    )
    for frame in data:
        out.write(frame)
    out.release()
    print("Video written succesfully")


@app.command()
def shoot(photo_dir: str = "./photos") -> None:
    """Captures the current frame from the camera."""
    with OpenCVCamera() as camera:
        data = camera.capture_frame()

    photo_dir_path = Path(photo_dir)
    photo_dir_path.mkdir(exist_ok=True, parents=True)

    current_timestamp: str = datetime.datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    filename: str = f"photo-{current_timestamp}.jpg"
    print(f"Saving file: {filename}...")

    res: bool = cv2.imwrite(photo_dir_path / filename, data)
    if res:
        print("Image written successfully")
    else:
        raise RuntimeError("Failed to write image")


if __name__ == "__main__":
    app()
