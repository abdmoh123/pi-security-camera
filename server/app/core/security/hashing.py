"""Module containing functions relating to hashing."""

from argon2 import PasswordHasher


def generate_hashed_password(
    password: str, hasher: PasswordHasher, salt: str | None = None, salt_encoding: str = "utf-8"
) -> str:
    """Converts a plaintext password to a hashed one, including the salt.

    NOTE: The salt must be at least 8 characters long.
    """
    encoded_salt: bytes | None = None
    if salt:
        encoded_salt = salt.encode(salt_encoding)
    hashed_password: str = hasher.hash(password, salt=encoded_salt)
    return f"{salt}:{hashed_password}"
