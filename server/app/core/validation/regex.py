"""Collection of regex rules used for validation."""

from typing import Literal

# As long as the name starts with a letter (case-insensitive)
camera_name_regex: Literal[r"^[a-zA-Z]+.*$"]
# Regex pattern for the ipv4 format
host_address_regex: Literal[r"^(((?!25?[6-9])[12]\d|[1-9])?\d\.?\b){4}$"]
# Regex pattern for the MAC address format
mac_address_regex: Literal[r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"]

# Regex pattern to match the email address format (doesn't check if it's real)
email_regex: Literal[r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$"]

# Passwords must be have the following:
# - At least 8 characters
# - At least 1 upper and 1 lower case letter
# - At least 1 number
# - At least 1 special character (one of these: @$!%*?&)
password_regex: Literal[r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"]

# Any name excluding '/' characters
file_name_regex: Literal[r"^[^\/\n]+$"]
