"""Pydantic request and response models for the API."""

from pydantic import BaseModel


class QueryRequest(BaseModel):
    """Request payload for `/query`."""

    question: str


class QueryResponse(BaseModel):
    """Response payload for `/query`."""

    answer: str
    confidence: float


class ConversationMessage(BaseModel):
    """Simple message schema for `/conversation`."""

    role: str
    content: str

