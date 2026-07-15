"""Test the user endpoint."""

from fastapi.testclient import TestClient


def test_read_current_user(client: TestClient) -> None:
    """Test the read users endpoint."""
    response = client.get("/api/v0/users/me")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "email": "user1@test.com", "is_admin": True}
