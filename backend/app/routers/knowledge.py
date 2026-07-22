from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.auth import User, require_role
from app.services.shared import rag_service

router = APIRouter(prefix="/knowledge", tags=["knowledge"])
service = rag_service


@router.post("/ingest")
def ingest_document(title: str, content: str, source: str = "uploaded", user: User = Depends(require_role("admin", "trainer"))) -> dict:
    chunk = service.ingest(title=title, content=content, source=source)
    return chunk.__dict__


@router.get("/search")
def search_knowledge(query: str, user: User = Depends(require_role("learner", "admin", "trainer"))) -> list[dict]:
    chunks = service.search(query)
    return [
        {
            "id": c.id,
            "title": c.title,
            "source": c.source,
            "preview": c.content[:400] if c.content else "",
            "content_length": len(c.content),
        }
        for c in chunks
    ]



@router.get("/all")
def list_knowledge(user: User = Depends(require_role("learner", "admin", "trainer"))) -> list[dict]:
    chunks = service.list_chunks()
    return [
        {
            "id": c.id,
            "title": c.title,
            "source": c.source,
            # Return a clean 400-char preview instead of raw binary content
            "preview": c.content[:400] if c.content else "",
            "content_length": len(c.content),
        }
        for c in chunks
    ]


@router.post("/upload")
def upload_documents(files: List[UploadFile] = File(...), user: User = Depends(require_role("admin", "trainer"))) -> list[dict]:
    ingested: list[dict] = []
    for file in files:
        raw = file.file.read()
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            # Try latin-1 fallback; strip control chars for cleanliness
            content = raw.decode("latin-1", errors="ignore")

        # Strip null bytes and excessive whitespace
        import re
        content = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", content)
        content = re.sub(r"\s{3,}", "\n\n", content).strip()

        chunk = service.ingest(title=file.filename or "Untitled", content=content, source="uploaded-file")
        ingested.append({"id": chunk.id, "title": chunk.title, "source": chunk.source, "content_length": len(chunk.content)})
    return ingested


@router.delete("/{chunk_id}")
def delete_knowledge_chunk(chunk_id: int, user: User = Depends(require_role("admin", "trainer"))) -> dict:
    deleted = service.delete_chunk(chunk_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Knowledge chunk {chunk_id} not found")
    return {"deleted": True, "chunk_id": chunk_id}

