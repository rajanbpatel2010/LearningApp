import os

from fastapi.testclient import TestClient

from app.main import app

os.environ["QUESTION_BANK_DB_PATH"] = ":memory:"
os.environ["RAG_DB_PATH"] = ":memory:"

client = TestClient(app)


def test_question_bank_import_and_search():
    token = client.post("/auth/login?username=demo&password=demo123").json()["access_token"]
    response = client.post(
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
    assert response.status_code == 200
    assert response.json()["count"] == 1

    search_response = client.get(
        "/question-bank/search?query=async",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert search_response.status_code == 200
    assert len(search_response.json()) == 1


def test_knowledge_ingest_and_search():
    token = client.post("/auth/login?username=demo&password=demo123").json()["access_token"]
    ingest_response = client.post(
        "/knowledge/ingest?title=Python Basics&content=Python is a high-level programming language",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert ingest_response.status_code == 200

    search_response = client.get(
        "/knowledge/search?query=Python",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert search_response.status_code == 200
    assert len(search_response.json()) >= 1
