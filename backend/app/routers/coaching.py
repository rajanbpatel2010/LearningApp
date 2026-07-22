from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth import User, require_role
from app.services.shared import evaluation_service, question_bank_service

router = APIRouter(prefix="/coaching", tags=["coaching"])


class AnswerRequest(BaseModel):
    question_id: int
    user_answer: str


@router.post("/evaluate")
def evaluate_answer(
    payload: AnswerRequest,
    user: User = Depends(require_role("learner", "admin", "trainer")),
) -> dict:
    """
    Evaluate a learner's answer against the stored expected answer and keywords.
    Returns a score (0–100), matched and missing keywords, and a feedback tip.
    """
    questions = question_bank_service.list_questions()
    question = next((q for q in questions if q.id == payload.question_id), None)

    if question is None:
        raise HTTPException(status_code=404, detail=f"Question {payload.question_id} not found")

    result = evaluation_service.evaluate(
        question_id=question.id,
        question_text=question.question_text,
        user_answer=payload.user_answer,
        expected_answer=question.expected_answer,
        keywords=question.keywords,
    )

    return {
        "question_id": result.question_id,
        "question_text": result.question_text,
        "user_answer": result.user_answer,
        "expected_answer": result.expected_answer,
        "score": result.score,
        "matched_keywords": result.matched_keywords,
        "missing_keywords": result.missing_keywords,
        "feedback": result.feedback,
    }
