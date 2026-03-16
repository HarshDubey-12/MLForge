"""Semantic chunking logic for splitting documents into retrieval units."""


class SemanticChunker:
    """Chunk text into semantically meaningful passages."""

    def chunk(self, text: str) -> list[str]:
        """Return chunked text spans."""
        if not text:
            return []
        return [text]

