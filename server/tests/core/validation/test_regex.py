"""Tests for regex patterns."""

import re

import app.core.validation.regex as regex_patterns


def test_email_regex() -> None:
    """Test the email regex pattern against valid emails."""
    test_emails = ["test@example.com", "test@gmail.com", "test@hotmail.com", "test@yahoo.co.uk", "test@protonmail.ch"]

    pattern = re.compile(regex_patterns.email_regex)
    assert all([pattern.match(email) for email in test_emails])
