"""Starter unit tests for the vector store repository."""

from ml_research_assistant.vector_store.faiss_store import FAISSVectorStore
from ml_research_assistant.vector_store.schemas import VectorRecord


def test_vector_store_add_and_search() -> None:
    store = FAISSVectorStore()
    store.add([[0.1] * 8], [VectorRecord(chunk_id="1", text="hello world")])
    results = store.search([0.1] * 8)
    assert len(results) == 1

