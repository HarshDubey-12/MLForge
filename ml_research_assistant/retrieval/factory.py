"""Factory helpers for composing retrieval strategies."""

from ml_research_assistant.retrieval.bm25_retriever import BM25Retriever
from ml_research_assistant.retrieval.hybrid_retriever import HybridRetriever


class RetrieverFactory:
    """Construct retrieval strategies from configuration."""

    @staticmethod
    def create_hybrid(semantic, keyword=None):
        """Create the default hybrid retriever."""
        return HybridRetriever(semantic=semantic, keyword=keyword or BM25Retriever())

