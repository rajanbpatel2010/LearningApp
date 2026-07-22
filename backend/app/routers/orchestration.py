from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.agents.orchestrator import Orchestrator
from app.auth import User, require_role
from app.services.shared import question_bank_service, rag_service, session_history_service

router = APIRouter(prefix="/orchestrator", tags=["orchestrator"])
orchestrator = Orchestrator()


class OrchestrationRequest(BaseModel):
    request: str


@router.post("/run")
def run_orchestrator(payload: OrchestrationRequest, user: User = Depends(require_role("learner", "admin", "trainer"))) -> dict:
    result = orchestrator.run(payload.request)
    return {
        "intent": result.intent,
        "summary": result.summary,
        "knowledge_hits": result.knowledge_hits,
        "question_hits": result.question_hits,
    }


class CoachingSessionRequest(BaseModel):
    request: str


@router.post("/session")
def start_coaching_session(payload: CoachingSessionRequest, user: User = Depends(require_role("learner", "admin", "trainer"))) -> dict:
    result = orchestrator.run(payload.request)
    record = session_history_service.record(payload.request, result.intent, result.summary)
    return {
        "status": "ready",
        "intent": result.intent,
        "summary": result.summary,
        "knowledge_hits": result.knowledge_hits,
        "question_hits": result.question_hits,
        "available_questions": len(question_bank_service.list_questions()),
        "available_knowledge_chunks": len(rag_service._chunks),
        "session_id": record.id,
    }


@router.get("/sessions")
def list_sessions(user: User = Depends(require_role("learner", "admin", "trainer"))) -> list[dict]:
    return [
        {
            "id": record.id,
            "request": record.request,
            "intent": record.intent,
            "summary": record.summary,
            "created_at": record.created_at,
        }
        for record in session_history_service.list_recent()
    ]
