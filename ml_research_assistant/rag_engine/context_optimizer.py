"""Context packing and token budget optimization logic."""


class ContextOptimizer:
    """Compress and order evidence before generation."""

    def optimize(self, contexts: list[dict[str, object]]) -> list[dict[str, object]]:
        """Return contexts trimmed to fit model constraints."""
        return contexts

