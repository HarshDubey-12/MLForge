"""Starter unit tests for retrieval strategies."""

from ml_research_assistant.embedding.service import EmbeddingService
from ml_research_assistant.retrieval.bm25_retriever import BM25Retriever
from ml_research_assistant.retrieval.hybrid_retriever import HybridRetriever
from ml_research_assistant.retrieval.semantic_retriever import SemanticRetriever
from ml_research_assistant.vector_store.faiss_store import FAISSVectorStore
from ml_research_assistant.vector_store.schemas import VectorRecord


def test_semantic_retriever_returns_results() -> None:
    embedding_service = EmbeddingService("stub-model")
    store = FAISSVectorStore()
    embedding = embedding_service.embed_documents(["attention is all you need"])[0]
    store.add([embedding], [VectorRecord(chunk_id="1", text="attention is all you need")])
    retriever = SemanticRetriever(embedding_service, store)
    assert retriever.retrieve("attention")


def test_hybrid_retriever_merges_keyword_and_semantic_results() -> None:
    embedding_service = EmbeddingService("stub-model")
    store = FAISSVectorStore()
    documents = [
        {"text": "attention is all you need", "metadata": {"title": "paper a"}},
        {"text": "transformers use self attention", "metadata": {"title": "paper b"}},
    ]
    embeddings = embedding_service.embed_documents([document["text"] for document in documents])
    store.add(
        embeddings,
        [
            VectorRecord(chunk_id=str(index), text=document["text"], metadata=document["metadata"])
            for index, document in enumerate(documents)
        ],
    )
    semantic = SemanticRetriever(embedding_service, store)
    keyword = BM25Retriever()
    keyword.index(documents)
    hybrid = HybridRetriever(semantic=semantic, keyword=keyword)

    assert hybrid.retrieve("attention", top_k=2)
