"""Sparse keyword retrieval powered by BM25."""

from ml_research_assistant.retrieval.base import RetrievalStrategy


class BM25Retriever(RetrievalStrategy):
    """Retrieve documents using lexical keyword matching."""

    def retrieve(self, query: str, top_k: int = 5) -> list[dict[str, object]]:
        """Return placeholder BM25 retrieval results."""
        return [{"text": f"BM25 result for: {query}", "score": 0.0}][:top_k]

