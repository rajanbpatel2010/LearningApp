from app.services.rag import RAGService


def test_search_ranks_related_keywords_without_exact_match():
    service = RAGService(db_path=":memory:")
    service.ingest(title="Concurrency notes", content="How async programming works in Python", source="test")
    service.ingest(title="Cooking guide", content="How to bake bread", source="test")

    results = service.search("parallel execution in python")

    assert results[0].title == "Concurrency notes"
    assert len(results) >= 1
