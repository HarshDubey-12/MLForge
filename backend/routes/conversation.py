"""Conversation endpoint for multi-turn assistant interactions."""

from fastapi import APIRouter, Depends

from backend.dependencies import get_rag_pipeline
from backend.schemas import ConversationMessage, ConversationResponse
from backend.services.conversation_service import ConversationService
from ml_research_assistant.rag_engine.pipeline import AdaptiveRAGPipeline


router = APIRouter(prefix="/conversation", tags=["conversation"])


def get_conversation_service(
    pipeline: AdaptiveRAGPipeline = Depends(get_rag_pipeline),
) -> ConversationService:
    """Provide the conversation service instance."""
    return ConversationService(pipeline=pipeline)


@router.post("", response_model=ConversationResponse)
def conversation(
    message: ConversationMessage,
    service: ConversationService = Depends(get_conversation_service),
) -> ConversationResponse:
    """Accept a conversation turn and return a placeholder response."""
    return service.reply(role=message.role, content=message.content)
