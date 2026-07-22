from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_knowledge_listing_returns_ingested_documents():
    token = client.post("/auth/login?username=demo&password=demo123").json()["access_token"]
    upload_response = client.post(
        "/knowledge/upload",
        files=[("files", ("management.txt", b"Management interview notes", "text/plain"))],
        headers={"Authorization": f"Bearer {token}"},
    )

    assert upload_response.status_code == 200

    list_response = client.get("/knowledge/all", headers={"Authorization": f"Bearer {token}"})
    assert list_response.status_code == 200
    assert any(item["title"] == "management.txt" for item in list_response.json())
