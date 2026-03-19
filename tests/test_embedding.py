"""Starter unit tests for embedding generation."""

from ml_research_assistant.embedding.service import EmbeddingService


def test_embed_query_returns_vector() -> None:
    service = EmbeddingService(model_name="stub-model")
    vector = service.embed_query("transformers")
    assert len(vector) > 0
    assert any(value != 0.0 for value in vector)
