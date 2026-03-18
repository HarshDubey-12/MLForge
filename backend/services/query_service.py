"""Service layer for research query execution."""

from backend.schemas import QueryResponse
from ml_research_assistant.rag_engine.pipeline import AdaptiveRAGPipeline


class QueryService:
    """Handle execution of the adaptive RAG pipeline for user questions."""

    def __init__(self, pipeline: AdaptiveRAGPipeline) -> None:
        self.pipeline = pipeline

    def run_query(self, question: str) -> QueryResponse:
        """Execute the pipeline and normalize the response payload."""
        result = self.pipeline.run(question)
        response = result["response"]

        return QueryResponse(
            answer=str(response["answer"]),
            confidence=float(response["confidence"]),
        )
