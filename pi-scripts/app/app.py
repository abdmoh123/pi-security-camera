"""Main endpoint of the application."""

from pathlib import Path

import typer

from app.core.cameras.opencv_camera import OpenCVCamera

app = typer.Typer()


@app.command()
def record() -> None:
    """Starts the camera recording routine."""
    with OpenCVCamera() as camera:
        camera.start_recording(Path(""))


if __name__ == "__main__":
    app()
