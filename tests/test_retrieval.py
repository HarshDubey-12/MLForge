"""Starter unit tests for retrieval strategies."""

from ml_research_assistant.embedding.service import EmbeddingService
from ml_research_assistant.retrieval.semantic_retriever import SemanticRetriever
from ml_research_assistant.vector_store.faiss_store import FAISSVectorStore
from ml_research_assistant.vector_store.schemas import VectorRecord


def test_semantic_retriever_returns_results() -> None:
    store = FAISSVectorStore()
    store.add([[0.0] * 8], [VectorRecord(chunk_id="1", text="attention is all you need")])
    retriever = SemanticRetriever(EmbeddingService("stub-model"), store)
    assert retriever.retrieve("attention")

