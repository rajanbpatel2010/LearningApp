import os

from app.services.question_bank import QuestionBankService
from app.services.rag import RAGService


def test_question_bank_persists_across_service_instances(tmp_path):
    db_path = tmp_path / "questions.db"

    first = QuestionBankService(str(db_path))
    first.import_questions(
        [
            {
                "category": "python",
                "topic": "async",
                "difficulty": "hard",
                "question_text": "What is async in Python?",
                "expected_answer": "It allows concurrent execution",
                "keywords": ["async", "python"],
            }
        ]
    )

    second = QuestionBankService(str(db_path))
    stored = second.list_questions()

    assert len(stored) == 1
    assert stored[0].question_text == "What is async in Python?"


def test_rag_persists_across_service_instances(tmp_path):
    db_path = tmp_path / "rag.db"

    first = RAGService(str(db_path))
    first.ingest("Python Basics", "Python is a high-level programming language")

    second = RAGService(str(db_path))
    hits = second.search("Python")

    assert len(hits) == 1
    assert hits[0].title == "Python Basics"
