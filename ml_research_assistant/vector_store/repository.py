"""Repository Pattern interface for vector storage backends."""

from abc import ABC, abstractmethod

from ml_research_assistant.vector_store.schemas import VectorRecord


class VectorRepository(ABC):
    """Abstract access layer for vector database operations."""

    @abstractmethod
    def add(self, embeddings: list[list[float]], records: list[VectorRecord]) -> None:
        """Persist embeddings and associated metadata."""

    @abstractmethod
    def search(self, query_embedding: list[float], top_k: int = 5) -> list[VectorRecord]:
        """Return the nearest records for the query embedding."""

