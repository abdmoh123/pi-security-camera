"""Tests for the hashing module."""

import pytest
from argon2 import PasswordHasher
from argon2.exceptions import HashingError

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


def test_short_salt() -> None:
    """Test if the software breaks if the salt is too short."""
    ph = PasswordHasher()
    salt: str = "1234"
    salt_encoding: str = "utf-8"

    test_password: str = "password"

    with pytest.raises(HashingError):
        _ = generate_hashed_password(test_password, ph, salt, salt_encoding)
