"""Enum for User columns."""

from enum import StrEnum, auto


class UserColumns(StrEnum):
    """Enum for User columns. Useful for sorting."""

    ID = auto()
    EMAIL = auto()
    REGISTERED_AT = auto()
