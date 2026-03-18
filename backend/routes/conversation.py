"""Conversation endpoint for multi-turn assistant interactions."""

from fastapi import APIRouter, Depends

from backend.schemas import ConversationMessage, ConversationResponse
from backend.services.conversation_service import ConversationService


router = APIRouter(prefix="/conversation", tags=["conversation"])


def get_conversation_service() -> ConversationService:
    """Provide the conversation service instance."""
    return ConversationService()


@router.post("", response_model=ConversationResponse)
def conversation(
    message: ConversationMessage,
    service: ConversationService = Depends(get_conversation_service),
) -> ConversationResponse:
    """Accept a conversation turn and return a placeholder response."""
    return service.reply(role=message.role, content=message.content)
