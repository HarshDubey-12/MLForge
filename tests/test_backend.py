"""Integration-style tests for the FastAPI backend."""

from fastapi.testclient import TestClient

from backend.app import create_app
from backend.routes.conversation import get_conversation_service
from backend.routes.query import get_query_service
from backend.schemas import ConversationResponse, QueryResponse


def test_health_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200


def test_query_endpoint_returns_evidence_payload() -> None:
    app = create_app()

    class StubQueryService:
        def run_query(self, question: str) -> QueryResponse:
            return QueryResponse(
                answer=f"Answer for {question}",
                confidence=0.77,
                plan_summary="Hybrid retrieval selected 2 contexts.",
                needs_revision=False,
                evidence=[
                    {
                        "chunk_id": "chunk-1",
                        "title": "Paper A",
                        "excerpt": "Useful excerpt",
                        "score": 0.91,
                        "sources": ["semantic", "keyword"],
                    }
                ],
            )

    app.dependency_overrides[get_query_service] = lambda: StubQueryService()
    client = TestClient(app)

    response = client.post("/query", json={"question": "What is RAG?"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["answer"] == "Answer for What is RAG?"
    assert payload["confidence"] == 0.77
    assert payload["evidence"][0]["title"] == "Paper A"


def test_conversation_endpoint_returns_evidence_payload() -> None:
    app = create_app()

    class StubConversationService:
        def reply(self, role: str, content: str) -> ConversationResponse:
            return ConversationResponse(
                reply=f"{role}: {content}",
                confidence=0.61,
                evidence=[
                    {
                        "chunk_id": "chunk-2",
                        "title": "Paper B",
                        "excerpt": "Follow-up evidence",
                        "score": 0.82,
                        "sources": ["semantic"],
                    }
                ],
            )

    app.dependency_overrides[get_conversation_service] = lambda: StubConversationService()
    client = TestClient(app)

    response = client.post("/conversation", json={"role": "user", "content": "Compare two papers"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["reply"] == "user: Compare two papers"
    assert payload["confidence"] == 0.61
    assert payload["evidence"][0]["title"] == "Paper B"
