"""Cross-encoder reranking for improving final retrieval order."""


class Reranker:
    """Rescore retrieved contexts before generation."""

    def rerank(self, query: str, documents: list[dict[str, object]]) -> list[dict[str, object]]:
        """Return reranked documents."""
        return documents

