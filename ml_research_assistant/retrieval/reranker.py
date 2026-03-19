"""Cross-encoder reranking for improving final retrieval order."""

import re


class Reranker:
    """Rescore retrieved contexts before generation."""

    def rerank(self, query: str, documents: list[dict[str, object]]) -> list[dict[str, object]]:
        """Return reranked documents using lexical overlap and incoming scores."""
        query_terms = set(re.findall(r"\b\w+\b", query.lower()))
        reranked: list[dict[str, object]] = []

        for document in documents:
            text = str(document.get("text", ""))
            text_terms = set(re.findall(r"\b\w+\b", text.lower()))
            overlap = len(query_terms & text_terms)
            base_score = float(document.get("score", 0.0))
            combined_score = base_score + overlap

            reranked.append({**document, "score": combined_score})

        return sorted(reranked, key=lambda item: float(item.get("score", 0.0)), reverse=True)
