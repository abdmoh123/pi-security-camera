"""Main SurveillanceSystem loop generic protocol."""

from typing import Protocol


class LoopPolicy(Protocol):
    """Main SurveillanceSystem loop protocol."""

    def run_loop(self) -> None:
        """Main loop for the surveillance system system."""
        ...
