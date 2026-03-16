"""Text normalization and cleanup for heterogeneous research sources."""


class DocumentCleaner:
    """Standardize whitespace, encoding artifacts, and boilerplate."""

    def clean(self, text: str) -> str:
        """Return cleaned document text."""
        return text.strip()

