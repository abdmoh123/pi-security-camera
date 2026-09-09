"""Enum for Camera columns."""

from enum import StrEnum, auto


class CameraColumns(StrEnum):
    """Enum for Camera columns. Useful for sorting."""

    ID = auto()
    NAME = auto()
    MAC_ADDRESS = auto()
    REGISTERED_AT = auto()
