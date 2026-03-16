"""Strategy Pattern base class for retrieval implementations."""

from abc import ABC, abstractmethod
from typing import Any


class RetrievalStrategy(ABC):
    """Common interface for interchangeable retrieval algorithms."""

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Return ranked contexts for a user query."""

