import os

from fastapi.testclient import TestClient

os.environ["QUESTION_BANK_DB_PATH"] = ":memory:"
os.environ["RAG_DB_PATH"] = ":memory:"

from app.main import app

client = TestClient(app)


def test_orchestrator_routes_request_to_correct_flow():
    token = client.post("/auth/login?username=demo&password=demo123").json()["access_token"]

    client.post(
        "/question-bank/import",
        json=[
            {
                "category": "python",
                "topic": "async",
                "difficulty": "hard",
                "question_text": "What is async in Python?",
                "expected_answer": "It allows concurrent execution",
                "keywords": ["async", "python"],
            }
        ],
        headers={"Authorization": f"Bearer {token}"},
    )

    client.post(
        "/knowledge/ingest?title=Python Basics&content=Python is a high-level programming language",
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.post(
        "/orchestrator/run",
        json={"request": "Prepare me for a Python interview"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["intent"] == "interview_coaching"
    assert response.json()["question_hits"]
