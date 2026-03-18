"""Dependency wiring for backend services."""

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
from ml_research_assistant.retrieval.factory import RetrieverFactory
from ml_research_assistant.retrieval.reranker import Reranker
from ml_research_assistant.retrieval.semantic_retriever import SemanticRetriever
from ml_research_assistant.vector_store.faiss_store import FAISSVectorStore


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
    repository = FAISSVectorStore()
    embedding_service = EmbeddingService(model_name="sentence-transformers/all-MiniLM-L6-v2")
    semantic = SemanticRetriever(embedding_service=embedding_service, repository=repository)
    retriever = RetrieverFactory.create_hybrid(semantic=semantic)
    return AdaptiveRAGPipeline(
        analyzer=QueryAnalyzer(),
        planner=RetrievalPlanner(),
        retriever=retriever,
        reranker=Reranker(),
        optimizer=ContextOptimizer(),
        estimator=UncertaintyEstimator(),
        generator=AnswerGenerator(model_name="your-fine-tuned-model"),
        evaluator=SelfEvaluator(),
    )
