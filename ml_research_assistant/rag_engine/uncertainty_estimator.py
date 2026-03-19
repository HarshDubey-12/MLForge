"""Confidence estimation for adaptive answer generation."""


class UncertaintyEstimator:
    """Estimate confidence from evidence quality and model signals."""

    def estimate(self, contexts: list[dict[str, object]]) -> float:
        """Estimate confidence from result count and score strength."""
        if not contexts:
            return 0.15

        scores = [float(context.get("score", 0.0)) for context in contexts[:5]]
        avg_score = sum(scores) / len(scores) if scores else 0.0
        context_factor = min(len(contexts) / 5.0, 1.0)
        normalized_score = avg_score / (avg_score + 2.0) if avg_score > 0 else 0.2
        confidence = 0.35 + (0.35 * context_factor) + (0.3 * normalized_score)
        return max(0.0, min(0.99, confidence))
