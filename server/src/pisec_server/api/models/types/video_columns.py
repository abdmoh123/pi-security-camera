"""Enum for Video columns."""

from enum import StrEnum, auto


class VideoColumns(StrEnum):
    """Enum for Video columns. Useful for sorting."""

    ID = auto()
    CAMERA_ID = auto()
    FILE_NAME = auto()
    UPLOADED_AT = auto()
