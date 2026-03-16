"""Starter unit tests for embedding generation."""

from ml_research_assistant.embedding.service import EmbeddingService


def test_embed_query_returns_vector() -> None:
    service = EmbeddingService(model_name="stub-model")
    assert len(service.embed_query("transformers")) == 8

