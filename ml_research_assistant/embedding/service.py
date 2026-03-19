"""SentenceTransformers-based embedding generation service."""

from ml_research_assistant.embedding.factory import EmbeddingModelFactory


class EmbeddingService:
    """Generate embeddings for document chunks and queries."""

    def __init__(self, model_name: str) -> None:
        self.model = EmbeddingModelFactory.create(model_name)

    def embed_documents(self, chunks: list[str]) -> list[list[float]]:
        """Return embeddings for a batch of document chunks."""
        if not chunks:
            return []

        embeddings = self.model.encode(
            chunks,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        """Return an embedding for a single query string."""
        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return embedding.tolist()
