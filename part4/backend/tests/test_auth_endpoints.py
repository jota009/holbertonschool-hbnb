# test_auth_endpoint.py

import pytest
from app import create_app
from flask import url_for

@pytest.fixture
def client():
    app = create_app("config.DevelopmentConfig")
    app.testing = True
    with app.test_client() as client:
        yield client

def register_user(client, email="test@example.com", pw="Test1234"):
    return client.post(
        "/api/v1/users/",
        json={
            "first_name": "Test",
            "last_name":  "User",
            "email":      email,
            "password":   pw,
            "is_admin":   False
        }
    )

def test_login_success(client):
    # 1) register first
    rv = register_user(client, "auth@example.com", "Secret123")
    assert rv.status_code == 201

    # 2) then log in
    rv = client.post(
        "/api/v1/auth/login",
        json={"email":"auth@example.com","password":"Secret123"}
    )
    assert rv.status_code == 200
    data = rv.get_json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)

def test_login_invalid_password(client):
    register_user(client, "nope@example.com", "RightPass")
    rv = client.post(
        "/api/v1/auth/login",
        json={"email":"nope@example.com","password":"WrongPass"}
    )
    assert rv.status_code == 401
    assert rv.get_json()["error"] == "Invalid credentials"

def test_login_unknown_user(client):
    rv = client.post(
        "/api/v1/auth/login",
        json={"email":"ghost@example.com","password":"Anything"}
    )
    assert rv.status_code == 401
    assert rv.get_json()["error"] == "Invalid credentials"
