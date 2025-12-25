"""Collection of regex rules used for validation."""

from typing import Literal

camera_name_regex: Literal[r"^[a-zA-Z]+.*$"]  # As long as the name starts with a letter (case-insensitive)
host_address_regex: Literal[r"^(((?!25?[6-9])[12]\d|[1-9])?\d\.?\b){4}$"]  # ipv4 pattern
mac_address_regex: Literal[r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"]
