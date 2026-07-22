from __future__ import annotations

from dataclasses import dataclass
from typing import List

from app.services.shared import question_bank_service, rag_service


@dataclass
class OrchestratorResponse:
    intent: str
    summary: str
    knowledge_hits: List[dict]
    question_hits: List[dict]


class Orchestrator:
    def __init__(self, rag_service_instance=None, question_service_instance=None) -> None:
        self.rag_service = rag_service_instance or rag_service
        self.question_service = question_service_instance or question_bank_service

    def classify_intent(self, user_request: str) -> str:
        lowered = user_request.lower()
        if any(keyword in lowered for keyword in ["interview", "mock", "question", "practice"]):
            return "interview_coaching"
        if any(keyword in lowered for keyword in ["learn", "explain", "concept", "study"]):
            return "learning"
        return "general"

    def run(self, user_request: str) -> OrchestratorResponse:
        intent = self.classify_intent(user_request)
        knowledge_hits = [chunk.__dict__ for chunk in self.rag_service.search(user_request)]
        expanded_query = user_request.lower()
        if intent == "interview_coaching":
            expanded_query = f"{expanded_query} interview python async question practice"
        question_hits = [question.__dict__ for question in self.question_service.search(expanded_query)]

        if intent == "interview_coaching":
            summary = (
                f"Interview coaching flow selected with {len(knowledge_hits)} knowledge match(es) and "
                f"{len(question_hits)} question match(es) for targeted practice."
            )
        elif knowledge_hits:
            summary = (
                f"Learning flow selected with {len(knowledge_hits)} knowledge match(es) to support your study."
            )
        else:
            summary = "General assistance flow selected with fallback guidance."

        return OrchestratorResponse(
            intent=intent,
            summary=summary,
            knowledge_hits=knowledge_hits,
            question_hits=question_hits,
        )
