"""Service layer for conversation interactions."""

from backend.schemas import ConversationResponse, EvidenceItem
from ml_research_assistant.rag_engine.pipeline import AdaptiveRAGPipeline


class ConversationService:
    """Handle multi-turn conversation responses."""

    def __init__(self, pipeline: AdaptiveRAGPipeline) -> None:
        self.pipeline = pipeline

    def reply(self, role: str, content: str) -> ConversationResponse:
        """Generate a response for a conversation turn using the shared RAG pipeline."""
        result = self.pipeline.run(content)
        response = result["response"]
        contexts = result.get("contexts", [])

        evidence = [
            EvidenceItem(
                chunk_id=(
                    str(context.get("chunk_id"))
                    if context.get("chunk_id") is not None
                    else None
                ),
                title=str(context.get("metadata", {}).get("title", "Untitled source")),
                excerpt=str(context.get("text", ""))[:220],
                score=float(context.get("score", 0.0)),
                sources=[
                    str(source)
                    for source in context.get("sources", [])
                    if str(source).strip()
                ],
            )
            for context in contexts[:3]
        ]

        prefix = "Research follow-up" if role == "user" else "System follow-up"
        return ConversationResponse(
            reply=f"{prefix}: {response['answer']}",
            confidence=float(response.get("confidence", 0.0)),
            evidence=evidence,
        )
