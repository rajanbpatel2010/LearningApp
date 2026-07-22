import os

from app.services.evaluation import EvaluationService
from app.services.question_bank import QuestionBankService
from app.services.rag import RAGService
from app.services.session_history import SessionHistoryService

QUESTION_BANK_DB_PATH = os.environ.get("QUESTION_BANK_DB_PATH", "question_bank.db")
RAG_DB_PATH = os.environ.get("RAG_DB_PATH", "rag.db")
SESSION_HISTORY_DB_PATH = os.environ.get("SESSION_HISTORY_DB_PATH", "session_history.db")

question_bank_service = QuestionBankService(QUESTION_BANK_DB_PATH)
rag_service = RAGService(RAG_DB_PATH)
session_history_service = SessionHistoryService(SESSION_HISTORY_DB_PATH)
evaluation_service = EvaluationService()
