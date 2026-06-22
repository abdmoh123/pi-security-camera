"""Stores configs or settings for the app."""

import os
from dataclasses import dataclass
from pathlib import Path

from app.services.factories.camera_factory import CameraType


@dataclass(frozen=True)
class Settings:
    """Stores configs or settings for the app."""

    data_dir: Path = Path(os.environ.get("DATA_DIR", "./data/"))
    camera_type: CameraType = CameraType(
        os.environ.get("CAMERA_TYPE", "opencv")
    )


settings = Settings()
