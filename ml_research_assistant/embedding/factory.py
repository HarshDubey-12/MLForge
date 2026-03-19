"""Factory Pattern for constructing embedding model clients."""

from __future__ import annotations

import hashlib

import numpy as np


class _FallbackEmbeddingModel:
    """Small deterministic encoder used for tests and offline fallback."""

    def __init__(self, dimension: int = 64) -> None:
        self.dimension = dimension

    def encode(
        self,
        inputs: str | list[str],
        convert_to_numpy: bool = True,
        normalize_embeddings: bool = True,
    ):
        texts = [inputs] if isinstance(inputs, str) else inputs
        vectors = np.asarray(
            [self._encode_text(text) for text in texts],
            dtype="float32",
        )

        if normalize_embeddings and len(vectors):
            norms = np.linalg.norm(vectors, axis=1, keepdims=True)
            norms[norms == 0.0] = 1.0
            vectors = vectors / norms

        if isinstance(inputs, str):
            return vectors[0] if convert_to_numpy else vectors[0].tolist()
        return vectors if convert_to_numpy else vectors.tolist()

    def _encode_text(self, text: str) -> list[float]:
        values = [0.0] * self.dimension
        tokens = text.lower().split()

        if not tokens:
            return values

        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            for index, byte in enumerate(digest):
                values[index % self.dimension] += byte / 255.0

        return values


class EmbeddingModelFactory:
    """Create embedding model adapters based on configuration."""

    @staticmethod
    def create(model_name: str):
        """Load and return an embedding model with a deterministic fallback."""
        if model_name == "stub-model":
            return _FallbackEmbeddingModel()

        try:
            from sentence_transformers import SentenceTransformer

            return SentenceTransformer(model_name)
        except Exception:
            return _FallbackEmbeddingModel()
