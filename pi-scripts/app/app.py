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
    print(f"Current timestamp: {current_timestamp}")

    fourcc: int = cv2.VideoWriter_fourcc(*"mp4v")

    print("Writing video...")
    out = cv2.VideoWriter(
        str(video_dir_path / f"{current_timestamp}.mp4"),
        fourcc,
        24.0,
        data[0].shape[1::-1],
    )
    for frame in data:
        out.write(frame)
    out.release()
    print("Video written succesfully")


if __name__ == "__main__":
    app()
