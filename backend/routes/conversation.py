"""Conversation endpoint for multi-turn assistant interactions."""

from fastapi import APIRouter

from backend.schemas import ConversationMessage


router = APIRouter(prefix="/conversation", tags=["conversation"])


@router.post("")
def conversation(message: ConversationMessage) -> dict[str, str]:
    """Accept a conversation turn and return a placeholder response."""
    return {"reply": f"Received message from {message.role}"}

