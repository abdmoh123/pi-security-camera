"""Camera types."""

from enum import StrEnum, auto


class CameraType(StrEnum):
    """Camera types."""

    OPENCV = auto()
    DUMMY = auto()
