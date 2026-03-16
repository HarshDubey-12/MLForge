"""Pipeline Pattern orchestration for the adaptive RAG engine."""

from ml_research_assistant.rag_engine.context_optimizer import ContextOptimizer
from ml_research_assistant.rag_engine.generator import AnswerGenerator
from ml_research_assistant.rag_engine.query_analyzer import QueryAnalyzer
from ml_research_assistant.rag_engine.retrieval_planner import RetrievalPlanner
from ml_research_assistant.rag_engine.self_evaluator import SelfEvaluator
from ml_research_assistant.rag_engine.uncertainty_estimator import UncertaintyEstimator
from ml_research_assistant.retrieval.base import RetrievalStrategy
from ml_research_assistant.retrieval.reranker import Reranker


class AdaptiveRAGPipeline:
    """Coordinate analysis, retrieval, generation, and evaluation."""

    def __init__(
        self,
        analyzer: QueryAnalyzer,
        planner: RetrievalPlanner,
        retriever: RetrievalStrategy,
        reranker: Reranker,
        optimizer: ContextOptimizer,
        estimator: UncertaintyEstimator,
        generator: AnswerGenerator,
        evaluator: SelfEvaluator,
    ) -> None:
        self.analyzer = analyzer
        self.planner = planner
        self.retriever = retriever
        self.reranker = reranker
        self.optimizer = optimizer
        self.estimator = estimator
        self.generator = generator
        self.evaluator = evaluator

    def run(self, query: str) -> dict[str, object]:
        """Execute the adaptive RAG workflow end to end."""
        analysis = self.analyzer.analyze(query)
        plan = self.planner.plan(analysis)
        contexts = self.retriever.retrieve(query, top_k=int(plan["top_k"]))
        reranked_contexts = self.reranker.rerank(query, contexts)
        optimized_contexts = self.optimizer.optimize(reranked_contexts)
        confidence = self.estimator.estimate(optimized_contexts)
        answer = self.generator.generate(query, optimized_contexts)
        evaluation = self.evaluator.evaluate(answer, confidence)
        return {"plan": plan, "contexts": optimized_contexts, "response": evaluation}

