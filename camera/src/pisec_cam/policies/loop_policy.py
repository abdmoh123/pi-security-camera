"""Main SurveillanceSystem loop generic protocol."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

from pisec_cam.surveillance_system import SurveillanceSystem


class LoopPolicy(Protocol):
    """Main SurveillanceSystem loop protocol."""

    @property
    def camera_system(self) -> SurveillanceSystem:
        """The camera state machine wrapper."""
        ...

    def run_loop(self) -> None:
        """Main loop for the surveillance system system."""
        ...


@dataclass(frozen=True)
class AbstractLoopPolicy(ABC):
    """Main SurveillanceSystem loop protocol."""

    camera_system: SurveillanceSystem

    @abstractmethod
    def run_loop(self) -> None:
        """Main loop for the surveillance system system."""
        ...
