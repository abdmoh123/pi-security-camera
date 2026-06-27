"""Stores configs or settings for the app."""

import os
from dataclasses import dataclass
from pathlib import Path

from app.services.factories.camera_factory import CameraType
from app.services.factories.loop_policy_factory import LoopPolicyType


@dataclass(frozen=True)
class Settings:
    """Stores configs or settings for the app."""

    data_dir: Path = Path(os.environ.get("DATA_DIR", "./data/"))
    camera_type: CameraType = CameraType(
        os.environ.get("CAMERA_TYPE", "opencv")
    )
    loop_policy_type: LoopPolicyType = LoopPolicyType(
        os.environ.get("LOOP_POLICY_TYPE", "api")
    )


settings = Settings()
