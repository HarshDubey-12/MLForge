"""Service layer for research query execution."""

from backend.schemas import EvidenceItem, QueryResponse
from ml_research_assistant.rag_engine.pipeline import AdaptiveRAGPipeline


class QueryService:
    """Handle execution of the adaptive RAG pipeline for user questions."""

    def __init__(self, pipeline: AdaptiveRAGPipeline) -> None:
        self.pipeline = pipeline

    def run_query(self, question: str) -> QueryResponse:
        """Execute the pipeline and normalize the response payload."""
        result = self.pipeline.run(question)
        response = result["response"]
        contexts = result.get("contexts", [])
        plan = result.get("plan", {})

        evidence = [
            EvidenceItem(
                chunk_id=(
                    str(context.get("chunk_id"))
                    if context.get("chunk_id") is not None
                    else None
                ),
                title=str(context.get("metadata", {}).get("title", "Untitled source")),
                excerpt=str(context.get("text", ""))[:320],
                score=float(context.get("score", 0.0)),
                sources=[
                    str(source)
                    for source in context.get("sources", [])
                    if str(source).strip()
                ],
            )
            for context in contexts[:5]
        ]

        return QueryResponse(
            answer=str(response["answer"]),
            confidence=float(response["confidence"]),
            plan_summary=(
                f"Hybrid retrieval selected top {plan.get('top_k', len(evidence) or 1)} "
                f"contexts for '{question[:80]}'."
            ),
            needs_revision=bool(response.get("needs_revision", False)),
            evidence=evidence,
        )
