"""Tests for utils package."""

import os
import re
import subprocess

from app.core.models.camera import mac_address_regex
from app.utils import get_mac_address


def test_get_mac_address() -> None:
    """Test the get_mac_address function."""
    mac_address = get_mac_address()

    assert len(mac_address) == 17
    assert re.match(mac_address_regex, mac_address)

    actual_mac_address_content = ""
    match os.name:
        case "posix":
            res = subprocess.run(
                ["ip", "link", "show"],
                capture_output=True,
                text=True,
            )
            if res.returncode != 0:
                raise Exception(res.stderr)

            actual_mac_address_content = res.stdout
        case "nt":
            res = subprocess.run(
                ["ipconfig", "/all"],
                capture_output=True,
                text=True,
            )
            if res.returncode != 0:
                raise Exception(res.stderr)

            split_stdout = res.stdout.split("\n")
            mac_address_lines = [
                line.replace("-", ":")
                for line in split_stdout
                if "Physical Address" in line
            ]
            actual_mac_address_content = "\n".join(mac_address_lines)
        case _:
            raise Exception("Unsupported platform")

    assert mac_address in actual_mac_address_content
