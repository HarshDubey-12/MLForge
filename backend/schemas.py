"""Pydantic request and response models for the API."""

from pydantic import BaseModel


class EvidenceItem(BaseModel):
    """A retrieved evidence item surfaced to the client."""

    chunk_id: str | None = None
    title: str
    excerpt: str
    score: float
    sources: list[str] = []


class QueryRequest(BaseModel):
    """Request payload for `/query`."""

    question: str


class QueryResponse(BaseModel):
    """Response payload for `/query`."""

    answer: str
    confidence: float
    plan_summary: str
    needs_revision: bool
    evidence: list[EvidenceItem]


class ConversationMessage(BaseModel):
    """Request payload for `/conversation`."""

    role: str
    content: str


class ConversationResponse(BaseModel):
    """Response payload for `/conversation`."""

    reply: str
    confidence: float | None = None
    evidence: list[EvidenceItem] = []


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
