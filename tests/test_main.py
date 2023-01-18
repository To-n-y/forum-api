from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK


def test_registration():
    response = client.get("/registration")
    assert response.status_code == status.HTTP_200_OK


def test_sign_in():
    response = client.get("/sign_in", params={"to": "1"})
    assert response.status_code == status.HTTP_200_OK


def test_sign_out():
    response = client.get("/sign_in", params={"to": "0"})
    assert response.status_code == status.HTTP_200_OK
