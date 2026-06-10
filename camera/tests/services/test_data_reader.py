"""Tests for the data reader module."""

from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from app.core.models.credential import Credential
from app.services.data_reader import DataReader


def test_DataReader_read_credentials(
    mocker: MockerFixture, tmp_path: Path
) -> None:
    """Check if the read function works normally."""
    client_id = "abdhawisa:aa5d2cb60eb740eeab9210e690a5a45d"
    user_id = 1
    client_secret = "0560e4066766d61d8f469f5da0a9f7847886a6afc09eeb96cdd64b693d9be7bde5cf26d920e4704a843d0c119b3717bc238e34e87a9afb26e7cd17e3e3881820"  # noqa: E501
    expected_credential = Credential(
        client_id=client_id, user_id=user_id, client_secret=client_secret
    )

    # A fake file is used
    mocked_file = f"""
{{
    "client_id": "{client_id}",
    "user_id": {user_id},
    "client_secret": "{client_secret}"
}}
"""

    # Disable the Path methods to prevent unimportant IO operations
    _ = mocker.patch.object(Path, "exists", return_value=True)
    _ = mocker.patch.object(Path, "read_text", return_value=mocked_file)

    data_reader = DataReader(tmp_path)

    assert data_reader.credentials_path == tmp_path / "credentials.json"

    actual_credential = data_reader.read_credentials()

    assert actual_credential == expected_credential


def test_DataReader_read_server_address(
    mocker: MockerFixture, tmp_path: Path
) -> None:
    """Check if the read function works normally."""
    expected_address = "http://localhost:8000"

    mocked_file = f"""
{expected_address}
"""

    # Disable the Path methods to prevent unimportant IO operations
    _ = mocker.patch.object(Path, "exists", return_value=True)
    _ = mocker.patch.object(Path, "read_text", return_value=mocked_file)

    data_reader = DataReader(tmp_path)

    assert data_reader.server_address_path == tmp_path / "server_address.txt"

    actual_address = data_reader.read_server_address()

    assert actual_address == expected_address


def test_DataReader_read_bad_server_address(
    mocker: MockerFixture, tmp_path: Path
) -> None:
    """Check if the read function fails on bad addresses."""
    test_address = "dumb fake address"

    mocked_file = f"""
{test_address}
"""

    # Disable the Path methods to prevent unimportant IO operations
    _ = mocker.patch.object(Path, "exists", return_value=True)
    _ = mocker.patch.object(Path, "read_text", return_value=mocked_file)

    data_reader = DataReader(tmp_path)

    with pytest.raises(ValueError):
        _ = data_reader.read_server_address()
