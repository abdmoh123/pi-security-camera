"""Tests for the hashing module."""

from argon2 import PasswordHasher

from app.core.security.hashing import generate_hashed_password


def test_generate_hashed_password() -> None:
    """Test the generate_hashed_password function."""
    ph = PasswordHasher()
    salt: str = "12345678"
    salt_encoding: str = "utf-8"

    test_password: str = "password"
    hashed_password = generate_hashed_password(test_password, ph, salt, salt_encoding)

    hash_without_salt: str = hashed_password.split(":")[1]
    assert ph.verify(hash=hash_without_salt, password=test_password)
