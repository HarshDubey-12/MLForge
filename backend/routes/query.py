"""Query endpoint for adaptive RAG inference."""

from fastapi import APIRouter, Depends

from backend.dependencies import get_rag_pipeline
from backend.schemas import QueryRequest, QueryResponse
from backend.services.query_service import QueryService
from ml_research_assistant.rag_engine.pipeline import AdaptiveRAGPipeline


router = APIRouter(prefix="/query", tags=["query"])


def get_query_service(
    pipeline: AdaptiveRAGPipeline = Depends(get_rag_pipeline),
) -> QueryService:
    """Provide the query service instance."""
    return QueryService(pipeline=pipeline)


@router.post("", response_model=QueryResponse)
def run_query(
    request: QueryRequest,
    service: QueryService = Depends(get_query_service),
) -> QueryResponse:
    """Execute the research assistant on a single user question."""
    return service.run_query(request.question)
