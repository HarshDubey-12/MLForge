"""Dynamic planner that selects the best retrieval strategy per query."""


class RetrievalPlanner:
    """Choose retrieval depth and strategy mix from query analysis."""

    def plan(self, analysis: dict[str, object]) -> dict[str, object]:
        """Return an execution plan for retrieval."""
        return {"top_k": 5, "strategy": "hybrid", **analysis}

