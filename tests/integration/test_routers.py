import pytest
from fastapi.testclient import TestClient

from app.main import application


@pytest.fixture
@pytest.mark.usefixtures("drop_db")
def client(drop_db):
    return TestClient(application)


@pytest.fixture
def token():
    return "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"


@pytest.fixture
def payload():
    return {"name": "Pythom Microservice Template", "document": "674.194.620-97", "active": True}


def test_welcome_router(client):
    expected_response = "Welcome to the Python Template API"
    response = client.get("/")

    assert response.status_code == 200
    assert expected_response in response.json()


def test_healthcheck_router(client):
    expected_response = {"status": "alive"}
    response = client.get("/healthcheck")

    assert response.status_code == 200
    assert response.json() == expected_response


def test_unauthorized_router_403(client, payload):
    response = client.post("/patner/", json=payload)

    assert response.status_code == 403
