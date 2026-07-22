from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_serves_frontend_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Learning Coach" in response.text
