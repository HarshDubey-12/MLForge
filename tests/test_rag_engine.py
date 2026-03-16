"""Starter unit tests for the RAG pipeline."""

from ml_research_assistant.rag_engine.context_optimizer import ContextOptimizer
from ml_research_assistant.rag_engine.generator import AnswerGenerator
from ml_research_assistant.rag_engine.pipeline import AdaptiveRAGPipeline
from ml_research_assistant.rag_engine.query_analyzer import QueryAnalyzer
from ml_research_assistant.rag_engine.retrieval_planner import RetrievalPlanner
from ml_research_assistant.rag_engine.self_evaluator import SelfEvaluator
from ml_research_assistant.rag_engine.uncertainty_estimator import UncertaintyEstimator
from ml_research_assistant.retrieval.bm25_retriever import BM25Retriever
from ml_research_assistant.retrieval.reranker import Reranker


def test_rag_pipeline_returns_response() -> None:
    pipeline = AdaptiveRAGPipeline(
        analyzer=QueryAnalyzer(),
        planner=RetrievalPlanner(),
        retriever=BM25Retriever(),
        reranker=Reranker(),
        optimizer=ContextOptimizer(),
        estimator=UncertaintyEstimator(),
        generator=AnswerGenerator(model_name="stub-generator"),
        evaluator=SelfEvaluator(),
    )
    result = pipeline.run("Explain contrastive learning.")
    assert "response" in result

