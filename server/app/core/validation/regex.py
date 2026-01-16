"""Collection of regex rules used for validation."""

# As long as the name starts with a letter (case-insensitive)
camera_name_regex: str = r"^[a-zA-Z]+.*$"
# Regex pattern for the ipv4 format
host_address_regex: str = r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$"
# Regex pattern for the MAC address format
mac_address_regex: str = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"

# Regex pattern to match the email address format (doesn't check if it's real)
email_regex: str = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$"

# Any name excluding '/' characters
file_name_regex: str = r"^[^\/\n]+$"
