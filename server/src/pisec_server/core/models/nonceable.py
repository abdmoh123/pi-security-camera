"""Any data structure that has a nonce and an expiry date."""

from datetime import datetime
from typing import Protocol


class Nonceable(Protocol):
    """A protocol for any token that has a nonce and an expiry date."""

    @property
    def nonce(self) -> str:
        """The nonce for a given token."""
        ...

    @property
    def expires_at(self) -> datetime:
        """An expiry date for the given token."""
        ...
