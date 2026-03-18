"""Service layer for conversation interactions."""

from backend.schemas import ConversationResponse


class ConversationService:
    """Handle multi-turn conversation responses."""

    def reply(self, role: str, content: str) -> ConversationResponse:
        """Generate a placeholder response for a conversation turn."""
        return ConversationResponse(reply=f"Received message from {role}: {content}")
