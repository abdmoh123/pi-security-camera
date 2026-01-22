"""Main test entrypoint."""

from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)


def test_read_root() -> None:
    """Root API function test."""
    response = client.get("/api/v0/")
    assert response.status_code == 200
    assert response.json() == {"message": app.title, "description": app.description, "version": app.version}


def test_check_health() -> None:
    """Health check API function test."""
    response = client.get("/api/v0/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
