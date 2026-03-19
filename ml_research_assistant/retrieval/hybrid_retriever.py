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

        merged: dict[str, dict[str, object]] = {}

        for rank, result in enumerate(semantic_results):
            text = str(result.get("text", "")).strip()
            if not text:
                continue

            score = float(result.get("score", 0.0))
            if score == 0.0:
                score = 1.0 / (rank + 1)

            merged[text] = {
                **result,
                "score": score,
                "sources": ["semantic"],
            }

        for rank, result in enumerate(keyword_results):
            text = str(result.get("text", "")).strip()
            if not text:
                continue

            score = float(result.get("score", 0.0))
            if score == 0.0:
                score = 1.0 / (rank + 1)

            if text in merged:
                merged[text]["score"] = float(merged[text]["score"]) + score
                merged[text]["sources"] = sorted(
                    set(merged[text].get("sources", [])) | {"keyword"}
                )
            else:
                merged[text] = {
                    **result,
                    "score": score,
                    "sources": ["keyword"],
                }

        ranked_results = sorted(
            merged.values(),
            key=lambda item: float(item.get("score", 0.0)),
            reverse=True,
        )

        return ranked_results[:top_k]
