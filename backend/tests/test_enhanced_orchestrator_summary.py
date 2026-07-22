from app.agents.orchestrator import Orchestrator


class FakeRAG:
    def search(self, query):
        return [type("Chunk", (), {"__dict__": {"id": 1, "title": "Python", "content": "Python basics", "source": "test"}})()]


class FakeQuestionBank:
    def search(self, query):
        return [type("Question", (), {"__dict__": {"id": 1, "category": "Python", "topic": "async", "difficulty": "medium", "question_text": "What is async?", "expected_answer": "A concurrent pattern", "keywords": ["async"], "source": "test"}})()]


def test_orchestrator_summary_includes_hit_counts():
    orchestrator = Orchestrator(rag_service_instance=FakeRAG(), question_service_instance=FakeQuestionBank())
    result = orchestrator.run("Prepare me for a Python interview")

    assert result.intent == "interview_coaching"
    assert "1 knowledge" in result.summary
    assert "1 question" in result.summary
