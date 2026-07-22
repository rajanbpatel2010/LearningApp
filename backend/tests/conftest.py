import pytest

from app.services.shared import question_bank_service, rag_service, session_history_service


@pytest.fixture(autouse=True)
def reset_services():
    question_bank_service._conn.execute("DELETE FROM questions")
    question_bank_service._conn.commit()
    question_bank_service._questions = []
    question_bank_service._next_id = 1

    rag_service._conn.execute("DELETE FROM knowledge_chunks")
    rag_service._conn.commit()
    rag_service._chunks = []
    rag_service._next_id = 1

    session_history_service._conn.execute("DELETE FROM session_history")
    session_history_service._conn.commit()

    yield

    question_bank_service._conn.execute("DELETE FROM questions")
    question_bank_service._conn.commit()
    question_bank_service._questions = []
    question_bank_service._next_id = 1

    rag_service._conn.execute("DELETE FROM knowledge_chunks")
    rag_service._conn.commit()
    rag_service._chunks = []
    rag_service._next_id = 1

    session_history_service._conn.execute("DELETE FROM session_history")
    session_history_service._conn.commit()
