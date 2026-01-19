"""Tests for the user validation module."""

import pytest

from app.core.validation.user_validation import password_validator


def test_password_validator() -> None:
    """Test the password validator on valid passwords."""
    valid_passwords: list[str] = [
        "Abc123!@#",
        "Abc123!@#Abc123!@#",
        "123abC!@f",
        "@@123AbcBN",
    ]

    [password_validator(password) for password in valid_passwords]


def test_invalid_password_validator() -> None:
    """Test the password validator against invalid passwords."""
    invalid_passwords: list[str] = [
        "abc123!@",
        "Abc123Abc123",
        "daDkabC!@",
        "@1Ac",
        "abcdefghijklmnopqrstuvwxyz",
        "1234567890",
        "@@@@@@@@",
        "ASDFGHJKL",
    ]

    with pytest.raises(ValueError):
        [password_validator(password) for password in invalid_passwords]
