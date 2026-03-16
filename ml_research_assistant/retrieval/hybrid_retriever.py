"""Hybrid retrieval that blends semantic and lexical signals."""

from ml_research_assistant.retrieval.base import RetrievalStrategy


class HybridRetriever(RetrievalStrategy):
    """Combine multiple strategies into a unified ranked result set."""

    def __init__(self, semantic: RetrievalStrategy, keyword: RetrievalStrategy) -> None:
        self.semantic = semantic
        self.keyword = keyword

    def retrieve(self, query: str, top_k: int = 5) -> list[dict[str, object]]:
        """Merge semantic and keyword retrieval outputs."""
        semantic_results = self.semantic.retrieve(query, top_k=top_k)
        keyword_results = self.keyword.retrieve(query, top_k=top_k)
        return (semantic_results + keyword_results)[:top_k]

