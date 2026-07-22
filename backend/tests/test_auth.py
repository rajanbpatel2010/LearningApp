from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_login_returns_token_for_valid_credentials():
    response = client.post("/auth/login?username=demo&password=demo123")
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_fails_for_invalid_credentials():
    response = client.post("/auth/login?username=demo&password=wrong")
    assert response.status_code == 401


def test_me_endpoint_requires_authentication():
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_admin_endpoint_requires_admin_role():
    response = client.get("/admin/ping")
    assert response.status_code == 401
