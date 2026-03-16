"""FAISS implementation of the vector repository."""

from ml_research_assistant.vector_store.repository import VectorRepository
from ml_research_assistant.vector_store.schemas import VectorRecord


class FAISSVectorStore(VectorRepository):
    """Concrete repository backed by a FAISS index."""

    def __init__(self) -> None:
        self._records: list[VectorRecord] = []

    def add(self, embeddings: list[list[float]], records: list[VectorRecord]) -> None:
        """Store records alongside future FAISS indexing hooks."""
        self._records.extend(records)

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[VectorRecord]:
        """Return placeholder nearest-neighbor results."""
        return self._records[:top_k]

