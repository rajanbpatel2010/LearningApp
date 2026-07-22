from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_endpoint_ingests_uploaded_files():
    token = client.post("/auth/login?username=demo&password=demo123").json()["access_token"]
    response = client.post(
        "/knowledge/upload",
        files=[("files", ("notes.txt", b"Python interview preparation notes", "text/plain"))],
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "notes.txt"
