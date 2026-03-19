"""Offline evaluation for retrieval grounding and answer quality."""

from __future__ import annotations

import json
import re
from pathlib import Path


class ModelEvaluator:
    """Evaluate the fine-tuned model against benchmark datasets."""

    def run(self, examples: list[dict[str, object]]) -> dict[str, float]:
        """Return lexical and grounding metrics for prediction/reference pairs."""
        if not examples:
            return {
                "average_f1": 0.0,
                "average_grounding": 0.0,
                "exact_match_rate": 0.0,
            }

        f1_scores = [self._f1(example) for example in examples]
        grounding_scores = [self._grounding_score(example) for example in examples]
        exact_matches = [
            1.0
            if str(example.get("prediction", "")).strip() == str(example.get("reference", "")).strip()
            else 0.0
            for example in examples
        ]

        return {
            "average_f1": sum(f1_scores) / len(f1_scores),
            "average_grounding": sum(grounding_scores) / len(grounding_scores),
            "exact_match_rate": sum(exact_matches) / len(exact_matches),
        }

    def run_from_jsonl(self, path: str | Path) -> dict[str, float]:
        """Load evaluation examples from JSONL and score them."""
        rows = [
            json.loads(line)
            for line in Path(path).read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        return self.run(rows)

    def _f1(self, example: dict[str, object]) -> float:
        prediction_tokens = self._tokenize(str(example.get("prediction", "")))
        reference_tokens = self._tokenize(str(example.get("reference", "")))

        if not prediction_tokens or not reference_tokens:
            return 0.0

        overlap = len(prediction_tokens & reference_tokens)
        if overlap == 0:
            return 0.0

        precision = overlap / max(len(prediction_tokens), 1)
        recall = overlap / max(len(reference_tokens), 1)
        return 2 * precision * recall / max(precision + recall, 1e-8)

    def _grounding_score(self, example: dict[str, object]) -> float:
        prediction_tokens = self._tokenize(str(example.get("prediction", "")))
        context_tokens = self._tokenize(str(example.get("context", "")))
        if not prediction_tokens or not context_tokens:
            return 0.0
        overlap = len(prediction_tokens & context_tokens)
        return overlap / max(len(prediction_tokens), 1)

    def _tokenize(self, text: str) -> set[str]:
        return set(re.findall(r"\b\w+\b", text.lower()))
