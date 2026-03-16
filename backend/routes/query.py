"""Query endpoint for adaptive RAG inference."""

from fastapi import APIRouter, Depends

from backend.dependencies import get_rag_pipeline
from backend.schemas import QueryRequest, QueryResponse


router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
def run_query(request: QueryRequest, pipeline=Depends(get_rag_pipeline)) -> QueryResponse:
    """Execute the research assistant on a single user question."""
    result = pipeline.run(request.question)
    response = result["response"]
    return QueryResponse(answer=str(response["answer"]), confidence=float(response["confidence"]))

