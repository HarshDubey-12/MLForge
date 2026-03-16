"""Semantic retrieval over dense embeddings."""

from ml_research_assistant.embedding.service import EmbeddingService
from ml_research_assistant.retrieval.base import RetrievalStrategy
from ml_research_assistant.vector_store.repository import VectorRepository


class SemanticRetriever(RetrievalStrategy):
    """Retrieve relevant chunks using embedding similarity."""

    def __init__(self, embedding_service: EmbeddingService, repository: VectorRepository) -> None:
        self.embedding_service = embedding_service
        self.repository = repository

    def retrieve(self, query: str, top_k: int = 5) -> list[dict[str, object]]:
        """Search the vector repository with a query embedding."""
        query_embedding = self.embedding_service.embed_query(query)
        return [
            {"text": record.text, "metadata": record.metadata}
            for record in self.repository.search(query_embedding, top_k=top_k)
        ]

