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
    """Request payload for `/conversation`."""

    role: str
    content: str


class ConversationResponse(BaseModel):
    """Response payload for `/conversation`."""

    reply: str


class UploadDocumentResponse(BaseModel):
    """Response payload for `/upload_documents`."""

    filename: str
    stored_filename: str
    stored_path: str
    content_type: str
    size_bytes: int
    status: str
    ingestion_status: str
    chunk_count: int
    metadata: dict[str, str]
