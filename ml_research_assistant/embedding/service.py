"""SentenceTransformers-based embedding generation service."""

from ml_research_assistant.embedding.factory import EmbeddingModelFactory


class EmbeddingService:
    """Generate embeddings for document chunks and queries."""

    def __init__(self, model_name: str) -> None:
        self.model = EmbeddingModelFactory.create(model_name)

    def embed_documents(self, chunks: list[str]) -> list[list[float]]:
        """Return placeholder document embeddings."""
        return [[0.0] * 8 for _ in chunks]

    def embed_query(self, query: str) -> list[float]:
        """Return a placeholder query embedding."""
        return [0.0] * 8

