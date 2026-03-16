"""Intent and complexity analysis for incoming user questions."""


class QueryAnalyzer:
    """Classify query type and detect retrieval needs."""

    def analyze(self, query: str) -> dict[str, object]:
        """Return structured signals used by downstream planners."""
        return {"query": query, "needs_retrieval": True}

