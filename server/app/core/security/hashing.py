"""Module containing functions relating to hashing."""

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError


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


def verify_password(plain_password: str, hashed_password: str, hasher: PasswordHasher) -> bool:
    """Verifies a plaintext password against a hashed password.

    The hashed_password is expected to be in the format 'salt:argon2_hash_string'.
    """
    hash_without_salt: str = hashed_password.split(":")[1]
    try:
        return hasher.verify(hash=hash_without_salt, password=plain_password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False
