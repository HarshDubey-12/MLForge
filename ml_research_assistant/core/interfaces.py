"""Shared protocol-style interfaces for clean architecture boundaries."""

from abc import ABC, abstractmethod
from typing import Any


class Service(ABC):
    """Minimal interface for application services."""

    @abstractmethod
    def healthcheck(self) -> dict[str, Any]:
        """Return the component status."""

