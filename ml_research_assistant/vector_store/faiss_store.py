"""FAISS implementation of the vector repository."""

from __future__ import annotations

import json
from pathlib import Path

import faiss
import numpy as np

from config.settings import settings
from ml_research_assistant.vector_store.repository import VectorRepository
from ml_research_assistant.vector_store.schemas import VectorRecord


class FAISSVectorStore(VectorRepository):
    """Concrete repository backed by a FAISS index."""

    def __init__(
        self,
        index_path: str | Path | None = None,
        records_path: str | Path | None = None,
    ) -> None:
        self.index_path = Path(index_path or settings.faiss_index_path)
        self.records_path = Path(records_path or f"{self.index_path}.records.json")
        self._records: list[VectorRecord] = []
        self._index: faiss.IndexFlatIP | None = None
        self._dimension: int | None = None
        self._load()

    def add(self, embeddings: list[list[float]], records: list[VectorRecord]) -> None:
        """Store embeddings and their associated records in a FAISS index."""
        if not embeddings:
            return

        if len(embeddings) != len(records):
            raise ValueError("Embeddings and records must have the same length.")

        matrix = np.asarray(embeddings, dtype="float32")
        if matrix.ndim != 2:
            raise ValueError("Embeddings must be a 2D list of floats.")

        dimension = matrix.shape[1]
        if self._index is None:
            self._dimension = dimension
            self._index = faiss.IndexFlatIP(dimension)
        elif dimension != self._dimension:
            raise ValueError(
                f"Embedding dimension mismatch: expected {self._dimension}, got {dimension}."
            )

        self._index.add(matrix)
        self._records.extend(records)
        self._persist()

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[VectorRecord]:
        """Return the nearest records for the query embedding."""
        if self._index is None or not self._records:
            return []

        query = np.asarray([query_embedding], dtype="float32")
        if query.ndim != 2:
            raise ValueError("Query embedding must be a 1D list of floats.")

        if query.shape[1] != self._dimension:
            raise ValueError(
                f"Query embedding dimension mismatch: expected {self._dimension}, got {query.shape[1]}."
            )

        limit = min(top_k, len(self._records))
        _, indices = self._index.search(query, limit)

        results: list[VectorRecord] = []
        for index in indices[0]:
            if 0 <= index < len(self._records):
                results.append(self._records[index])

        return results

    def get_all_records(self) -> list[VectorRecord]:
        """Return all indexed records for downstream indexing flows."""
        return list(self._records)

    @property
    def dimension(self) -> int | None:
        """Return the active vector dimension, if the store is initialized."""
        return self._dimension

    def is_empty(self) -> bool:
        """Return whether the index currently holds any records."""
        return not self._records

    def clear(self) -> None:
        """Reset the in-memory and on-disk index contents."""
        self._records = []
        self._index = None
        self._dimension = None

        if self.index_path.exists():
            self.index_path.unlink()
        if self.records_path.exists():
            self.records_path.unlink()

    def _persist(self) -> None:
        """Persist the FAISS index and metadata sidecar to disk."""
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.records_path.parent.mkdir(parents=True, exist_ok=True)

        if self._index is not None:
            faiss.write_index(self._index, str(self.index_path))

        self.records_path.write_text(
            json.dumps(
                [
                    {
                        "chunk_id": record.chunk_id,
                        "text": record.text,
                        "metadata": record.metadata,
                    }
                    for record in self._records
                ],
                indent=2,
            ),
            encoding="utf-8",
        )

    def _load(self) -> None:
        """Load the FAISS index and sidecar metadata if present."""
        if self.index_path.exists():
            self._index = faiss.read_index(str(self.index_path))
            self._dimension = self._index.d

        if self.records_path.exists():
            payload = json.loads(self.records_path.read_text(encoding="utf-8"))
            self._records = [
                VectorRecord(
                    chunk_id=item["chunk_id"],
                    text=item["text"],
                    metadata=item.get("metadata", {}),
                )
                for item in payload
            ]
