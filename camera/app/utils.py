"""Miscellaneous utility functions."""


def get_mac_address() -> str:
    """Get the MAC address of the current machine.

    Returns:
        The MAC address.
    """
    import uuid

    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e : e + 2] for e in range(0, 11, 2)])
