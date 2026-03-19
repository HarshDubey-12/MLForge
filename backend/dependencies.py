"""Dependency wiring for backend services."""

from __future__ import annotations

from functools import lru_cache

from config.settings import settings
from database.connection import get_session_factory, initialize_database
from database.repository import MetadataRepository
from ml_research_assistant.data_pipeline.document_cleaner import DocumentCleaner
from ml_research_assistant.data_pipeline.metadata_extractor import MetadataExtractor
from ml_research_assistant.data_pipeline.pdf_parser import PDFParser
from ml_research_assistant.data_pipeline.pipeline import DataIngestionPipeline
from ml_research_assistant.data_pipeline.semantic_chunker import SemanticChunker
from ml_research_assistant.embedding.service import EmbeddingService
from ml_research_assistant.rag_engine.context_optimizer import ContextOptimizer
from ml_research_assistant.rag_engine.generator import AnswerGenerator
from ml_research_assistant.rag_engine.pipeline import AdaptiveRAGPipeline
from ml_research_assistant.rag_engine.query_analyzer import QueryAnalyzer
from ml_research_assistant.rag_engine.retrieval_planner import RetrievalPlanner
from ml_research_assistant.rag_engine.self_evaluator import SelfEvaluator
from ml_research_assistant.rag_engine.uncertainty_estimator import UncertaintyEstimator
from ml_research_assistant.retrieval.bm25_retriever import BM25Retriever
from ml_research_assistant.retrieval.factory import RetrieverFactory
from ml_research_assistant.retrieval.reranker import Reranker
from ml_research_assistant.retrieval.semantic_retriever import SemanticRetriever
from ml_research_assistant.vector_store.faiss_store import FAISSVectorStore

initialize_database()


@lru_cache(maxsize=1)
def get_session_factory_cached():
    """Return the shared database session factory."""
    return get_session_factory()


@lru_cache(maxsize=1)
def get_metadata_repository() -> MetadataRepository:
    """Return the shared metadata repository instance."""
    return MetadataRepository(get_session_factory_cached())


@lru_cache(maxsize=1)
def get_vector_store() -> FAISSVectorStore:
    """Return the shared vector store instance."""
    return FAISSVectorStore()


@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
    """Return the shared embedding service instance."""
    return EmbeddingService(model_name=settings.embedding_model)


@lru_cache(maxsize=1)
def get_keyword_retriever() -> BM25Retriever:
    """Return the shared BM25 retriever instance."""
    return BM25Retriever()


@lru_cache(maxsize=1)
def get_semantic_retriever() -> SemanticRetriever:
    """Return the semantic retriever bound to the shared store and embedder."""
    return SemanticRetriever(
        embedding_service=get_embedding_service(),
        repository=get_vector_store(),
    )


_RETRIEVAL_BOOTSTRAPPED = False


def _bootstrap_retrieval_state() -> None:
    """Ensure persisted retrieval artifacts match the active embedding model."""
    global _RETRIEVAL_BOOTSTRAPPED
    if _RETRIEVAL_BOOTSTRAPPED:
        return

    metadata_repository = get_metadata_repository()
    vector_store = get_vector_store()
    embedding_service = get_embedding_service()
    keyword_retriever = get_keyword_retriever()

    existing_records = metadata_repository.get_vector_records()
    if existing_records:
        sample_embedding = embedding_service.embed_query("bootstrap dimension probe")
        expected_dimension = len(sample_embedding)

        if vector_store.dimension not in (None, expected_dimension):
            vector_store.clear()

        if vector_store.is_empty():
            embeddings = embedding_service.embed_documents([record.text for record in existing_records])
            vector_store.add(embeddings, existing_records)

    keyword_retriever.index(metadata_repository.get_keyword_documents())
    _RETRIEVAL_BOOTSTRAPPED = True


def get_data_ingestion_pipeline() -> DataIngestionPipeline:
    """Build the default document ingestion pipeline."""
    return DataIngestionPipeline(
        parser=PDFParser(),
        cleaner=DocumentCleaner(),
        chunker=SemanticChunker(),
        metadata_extractor=MetadataExtractor(),
    )


def get_rag_pipeline() -> AdaptiveRAGPipeline:
    """Build the default application pipeline."""
    _bootstrap_retrieval_state()
    hybrid_retriever = RetrieverFactory.create_hybrid(
        semantic=get_semantic_retriever(),
        keyword=get_keyword_retriever(),
    )
    return AdaptiveRAGPipeline(
        analyzer=QueryAnalyzer(),
        planner=RetrievalPlanner(),
        retriever=hybrid_retriever,
        reranker=Reranker(),
        optimizer=ContextOptimizer(),
        estimator=UncertaintyEstimator(),
        generator=AnswerGenerator(model_name=settings.generator_model),
        evaluator=SelfEvaluator(),
    )
