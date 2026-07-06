"""Enum for loop policy types."""

from enum import StrEnum, auto


class LoopPolicyType(StrEnum):
    """Enum for selecting the type of loop policy."""

    API = auto()
    OFFLINE = auto()
