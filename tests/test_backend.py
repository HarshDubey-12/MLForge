"""Starter unit tests for the FastAPI backend."""

from fastapi.testclient import TestClient

from backend.app import create_app


def test_health_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200

