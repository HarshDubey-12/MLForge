"""Build supervised and preference datasets from curated research corpora."""

from __future__ import annotations

import json
import random
import re
from dataclasses import dataclass
from pathlib import Path

from config.settings import settings


@dataclass
class DatasetSplitSummary:
    """Summary of generated dataset split files."""

    train_path: Path
    validation_path: Path
    test_path: Path
    total_examples: int


class DatasetPreparationJob:
    """Prepare fine-tuning-ready instruction datasets."""

    def __init__(
        self,
        output_dir: str | Path | None = None,
        train_ratio: float = 0.8,
        validation_ratio: float = 0.1,
        seed: int = 7,
    ) -> None:
        self.output_dir = Path(output_dir or settings.training_dataset_dir)
        self.train_ratio = train_ratio
        self.validation_ratio = validation_ratio
        self.seed = seed

    def run(
        self,
        records: list[dict[str, object]],
        dataset_name: str = "research_assistant",
    ) -> DatasetSplitSummary:
        """Transform raw records into train/validation/test JSONL files."""
        examples = [self._normalize_record(record) for record in records if self._normalize_record(record)]
        if not examples:
            raise ValueError("No usable training examples were produced.")

        random.Random(self.seed).shuffle(examples)

        train_end = max(1, int(len(examples) * self.train_ratio))
        validation_end = train_end + max(1, int(len(examples) * self.validation_ratio))
        if validation_end >= len(examples):
            validation_end = len(examples) - 1

        train_split = examples[:train_end]
        validation_split = examples[train_end:validation_end]
        test_split = examples[validation_end:]

        if not validation_split:
            validation_split = train_split[:1]
        if not test_split:
            test_split = validation_split[:1]

        dataset_dir = self.output_dir / dataset_name
        dataset_dir.mkdir(parents=True, exist_ok=True)

        train_path = dataset_dir / "train.jsonl"
        validation_path = dataset_dir / "validation.jsonl"
        test_path = dataset_dir / "test.jsonl"

        self._write_jsonl(train_path, train_split)
        self._write_jsonl(validation_path, validation_split)
        self._write_jsonl(test_path, test_split)

        manifest = dataset_dir / "manifest.json"
        manifest.write_text(
            json.dumps(
                {
                    "dataset_name": dataset_name,
                    "total_examples": len(examples),
                    "train_examples": len(train_split),
                    "validation_examples": len(validation_split),
                    "test_examples": len(test_split),
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        return DatasetSplitSummary(
            train_path=train_path,
            validation_path=validation_path,
            test_path=test_path,
            total_examples=len(examples),
        )

    def _normalize_record(self, record: dict[str, object]) -> dict[str, object] | None:
        """Normalize a raw chunk or QA record into a supervised example."""
        if "instruction" in record and "output" in record:
            return {
                "instruction": str(record["instruction"]),
                "input": str(record.get("input", "")),
                "output": str(record["output"]),
                "metadata": record.get("metadata", {}),
            }

        text = str(record.get("text", "")).strip()
        if not text:
            return None

        title = str(record.get("metadata", {}).get("title", "research document"))
        summary = self._summarize_text(text)
        return {
            "instruction": "Answer the question using the provided research passage.",
            "input": f"Title: {title}\nPassage: {text}",
            "output": summary,
            "metadata": record.get("metadata", {}),
        }

    def _summarize_text(self, text: str) -> str:
        """Create a compact target answer from a chunk of research text."""
        sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+", text)
            if sentence.strip()
        ]
        if not sentences:
            return text[:240]
        return " ".join(sentences[:2])[:320]

    def _write_jsonl(self, path: Path, rows: list[dict[str, object]]) -> None:
        """Write a list of dictionaries as JSONL."""
        path.write_text(
            "\n".join(json.dumps(row, ensure_ascii=True) for row in rows),
            encoding="utf-8",
        )
