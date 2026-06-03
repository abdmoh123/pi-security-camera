"""Stores configs or settings for the app."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Stores configs or settings for the app."""

    data_dir: Path = Path(os.environ.get("DATA_DIR", "./data/"))


settings = Settings()
