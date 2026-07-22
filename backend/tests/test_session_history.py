import os

from fastapi.testclient import TestClient

os.environ["QUESTION_BANK_DB_PATH"] = ":memory:"
os.environ["RAG_DB_PATH"] = ":memory:"
os.environ["SESSION_HISTORY_DB_PATH"] = ":memory:"

from app.main import app

client = TestClient(app)


def test_session_history_is_recorded_and_listed():
    token = client.post("/auth/login?username=demo&password=demo123").json()["access_token"]

    response = client.post(
        "/orchestrator/session",
        json={"request": "Prepare me for a Python interview"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ready"

    sessions_response = client.get(
        "/orchestrator/sessions",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert sessions_response.status_code == 200
    payload = sessions_response.json()
    assert len(payload) >= 1
    assert payload[0]["request"] == "Prepare me for a Python interview"
    assert payload[0]["intent"] == "interview_coaching"
