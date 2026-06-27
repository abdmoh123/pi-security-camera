"""Tests for utils package."""

import re
import subprocess

from app.core.models.camera import mac_address_regex
from app.utils import get_mac_address


def test_get_mac_address() -> None:
    """Test the get_mac_address function."""
    mac_address = get_mac_address()

    assert len(mac_address) == 17
    assert re.match(mac_address_regex, mac_address)

    res = subprocess.run(
        ["ip", "link", "show", "eth0"],
        capture_output=True,
        text=True,
    )
    if res.returncode != 0:
        raise Exception(res.stderr)

    assert mac_address in res.stdout
