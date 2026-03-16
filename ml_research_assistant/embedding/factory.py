"""Factory Pattern for constructing embedding model clients."""


class EmbeddingModelFactory:
    """Create embedding model adapters based on configuration."""

    @staticmethod
    def create(model_name: str) -> str:
        """Return a model handle placeholder."""
        return model_name

