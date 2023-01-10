import pytest
from fastapi.testclient import TestClient

from app.main import application


@pytest.fixture
@pytest.mark.usefixtures("drop_db")
def client(drop_db):
    return TestClient(application)


@pytest.fixture
def token():
    return "dddeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"


def test_welcome_router(client):
    expected_response = "For more information, read the documentation in /docs or /redoc"
    response = client.get("/")

    assert response.status_code == 200
    assert expected_response in response.json()


def test_healthcheck_router(client):
    expected_response = {"status": "alive"}
    response = client.get("/healthcheck")

    assert response.status_code == 200
    assert response.json() == expected_response


def test_unauthorized_router_403(client):
    response = client.get("/legacy/financing-formalized/formalizations/2023-01-06/fidc_v")

    assert response.status_code == 403
