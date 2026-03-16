"""Typed data models for indexed chunks and search results."""

from dataclasses import dataclass, field


@dataclass
class VectorRecord:
    """Represents an indexed chunk and its metadata."""

    chunk_id: str
    text: str
    metadata: dict[str, str] = field(default_factory=dict)

