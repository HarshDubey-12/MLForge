"""Sparse keyword retrieval powered by BM25."""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

from config.settings import settings
from ml_research_assistant.retrieval.base import RetrievalStrategy

try:
    from rank_bm25 import BM25Okapi
except Exception:  # pragma: no cover - exercised only when optional dependency is missing
    class BM25Okapi:  # type: ignore[override]
        """Small fallback BM25 implementation for offline and test environments."""

        def __init__(self, corpus: list[list[str]]) -> None:
            self.corpus = corpus
            self.doc_freqs = Counter()
            self.doc_lengths = [len(document) for document in corpus]
            self.avgdl = (
                sum(self.doc_lengths) / len(self.doc_lengths)
                if self.doc_lengths
                else 0.0
            )

            for document in corpus:
                for token in set(document):
                    self.doc_freqs[token] += 1

        def get_scores(self, query_tokens: list[str]) -> list[float]:
            """Return fallback BM25-like scores."""
            scores: list[float] = []
            total_documents = len(self.corpus)
            k1 = 1.5
            b = 0.75

            for document, doc_length in zip(self.corpus, self.doc_lengths):
                term_counts = Counter(document)
                score = 0.0
                for token in query_tokens:
                    if token not in term_counts:
                        continue

                    document_frequency = self.doc_freqs.get(token, 0)
                    idf = math.log(
                        1 + (total_documents - document_frequency + 0.5) / (document_frequency + 0.5)
                    )
                    tf = term_counts[token]
                    denominator = tf + k1 * (1 - b + b * doc_length / max(self.avgdl, 1.0))
                    score += idf * ((tf * (k1 + 1)) / denominator)

                scores.append(score)

            return scores


class BM25Retriever(RetrievalStrategy):
    """Retrieve documents using lexical keyword matching."""

    def __init__(self, corpus_path: str | Path | None = None) -> None:
        self.corpus_path = Path(corpus_path or settings.bm25_corpus_path)
        self._documents: list[dict[str, object]] = []
        self._tokenized_corpus: list[list[str]] = []
        self._bm25: BM25Okapi | None = None
        self._load()

    def index(self, documents: list[dict[str, object]]) -> None:
        """Index a set of text documents for lexical retrieval."""
        self._documents = documents
        self._tokenized_corpus = [
            self._tokenize(str(document.get("text", ""))) for document in documents
        ]
        if self._tokenized_corpus:
            self._bm25 = BM25Okapi(self._tokenized_corpus)
        else:
            self._bm25 = None
        self._persist()

    def retrieve(self, query: str, top_k: int = 5) -> list[dict[str, object]]:
        """Return top BM25-ranked documents for the query."""
        if not self._bm25 or not self._documents:
            return []

        query_tokens = self._tokenize(query)
        scores = self._bm25.get_scores(query_tokens)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True,
        )[:top_k]

        results: list[dict[str, object]] = []
        for index in ranked_indices:
            document = dict(self._documents[index])
            document["score"] = float(scores[index])
            results.append(document)

        return results

    def is_empty(self) -> bool:
        """Return whether the BM25 corpus is empty."""
        return not self._documents

    def _persist(self) -> None:
        """Persist the BM25 corpus documents to disk."""
        self.corpus_path.parent.mkdir(parents=True, exist_ok=True)
        self.corpus_path.write_text(json.dumps(self._documents, indent=2), encoding="utf-8")

    def _load(self) -> None:
        """Load the persisted BM25 corpus if it exists."""
        if not self.corpus_path.exists():
            return

        self._documents = json.loads(self.corpus_path.read_text(encoding="utf-8"))
        self._tokenized_corpus = [
            self._tokenize(str(document.get("text", ""))) for document in self._documents
        ]
        if self._tokenized_corpus:
            self._bm25 = BM25Okapi(self._tokenized_corpus)

    def _tokenize(self, text: str) -> list[str]:
        """Convert text into normalized BM25 tokens."""
        return re.findall(r"\b\w+\b", text.lower())
