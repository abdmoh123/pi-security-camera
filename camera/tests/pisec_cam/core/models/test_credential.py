"""Tests for the Credential model."""

import pytest

from pisec_cam.core.models.credential import Credential


def test_credential_validator() -> None:
    """Smoke test the validation for the Credentials class.

    Includes testing the client ID validator.
    """
    client_ids: list[str] = [
        "abdhawisa:5844a9af95e84ce193a978eb96bf2ac3",
        "user2:alskjdf23480hrfpuqwi3bfp9293g4fh",
        "a:1",
    ]

    test_user_id = 1
    test_secret = "secret"

    # No error should occur here
    credentials = [
        Credential(
            client_id=client_id, user_id=test_user_id, client_secret=test_secret
        )
        for client_id in client_ids
    ]

    # Check if the client IDs are the same
    res_client_ids = [credential.client_id for credential in credentials]
    assert res_client_ids == client_ids

    # Check if the user IDs are the same
    res_user_ids = [credential.user_id for credential in credentials]
    assert res_user_ids == [test_user_id] * len(client_ids)

    res_secrets = [credential.client_secret for credential in credentials]
    assert res_secrets == [test_secret] * len(client_ids)


def test_credential_invalid_client_id() -> None:
    """Smoke test invalid client IDs for the Credential class."""
    invalid_client_ids = ["abdhawisa", "user2:", ":asf234a2us"]

    for invalid_client_id in invalid_client_ids:
        with pytest.raises(ValueError):
            _ = Credential(
                client_id=invalid_client_id, user_id=1, client_secret="secret"
            )


def test_credential_get_user_name_quick() -> None:
    """Test the get_user_name_quick method."""
    client_ids: list[str] = [
        "abdhawisa:5844a9af95e84ce193a978eb96bf2ac3",
        "user2:alskjdf23480hrfpuqwi3bfp9293g4fh",
        "a:1",
    ]
    user_names: list[str] = [
        "abdhawisa",
        "user2",
        "a",
    ]

    test_secret = "secret"
    test_user_id = 1

    credentials = [
        Credential(
            client_id=client_id, user_id=test_user_id, client_secret=test_secret
        )
        for client_id in client_ids
    ]

    res_usernames = [
        credential.get_user_name_quick() for credential in credentials
    ]

    assert res_usernames == user_names
