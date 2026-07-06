"""Enums used by the camera FSM."""

from enum import StrEnum, auto


class CameraState(StrEnum):
    """The states of the camera."""

    DETECTING = auto()
    RECORDING = auto()
    SAVING = auto()
    SLEEPING = auto()
    STOPPED = auto()


class CameraEvent(StrEnum):
    """The events of the camera."""

    RECORD = auto()
    SAVE = auto()
    SLEEP = auto()
    WAKE = auto()
    STOP = auto()
