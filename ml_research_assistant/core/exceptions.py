"""Custom exception hierarchy for domain and infrastructure errors."""


class MLResearchAssistantError(Exception):
    """Base exception for the project."""


class RetrievalError(MLResearchAssistantError):
    """Raised when retrieval steps fail."""


class ConfigurationError(MLResearchAssistantError):
    """Raised when required configuration is missing or invalid."""

