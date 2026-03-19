"""Unit tests for training workflows."""

import json
from pathlib import Path

from ml_research_assistant.training.dataset_preparation import DatasetPreparationJob
from ml_research_assistant.training.evaluation import ModelEvaluator
from ml_research_assistant.training.qlora_finetune import QLoRAFineTuner


def test_dataset_preparation_job_writes_jsonl_splits() -> None:
    output_dir = Path("tests") / ".tmp" / "training_datasets"
    job = DatasetPreparationJob(output_dir=output_dir)
    summary = job.run(
        [
            {"text": "Attention helps models focus on important tokens.", "metadata": {"title": "doc-a"}},
            {"text": "Transformers scale well for sequence modeling.", "metadata": {"title": "doc-b"}},
            {"text": "Hybrid retrieval blends lexical and semantic evidence.", "metadata": {"title": "doc-c"}},
        ],
        dataset_name="unit_test_dataset",
    )

    assert summary.train_path.exists()
    assert summary.validation_path.exists()
    assert summary.test_path.exists()


def test_model_evaluator_scores_prediction_examples() -> None:
    evaluator = ModelEvaluator()
    metrics = evaluator.run(
        [
            {
                "prediction": "attention helps models focus",
                "reference": "attention helps models focus on tokens",
                "context": "attention helps models focus on relevant tokens",
            }
        ]
    )

    assert metrics["average_f1"] > 0.0
    assert metrics["average_grounding"] > 0.0


def test_qlora_finetuner_dry_run_writes_plan() -> None:
    dataset_dir = Path("tests") / ".tmp" / "qlora_dataset"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    for split in ("train", "validation"):
        (dataset_dir / f"{split}.jsonl").write_text(
            json.dumps(
                {
                    "instruction": "Summarize the passage.",
                    "input": "Passage: attention helps models focus.",
                    "output": "Attention helps models focus on relevant information.",
                }
            ),
            encoding="utf-8",
        )

    output_dir = Path("tests") / ".tmp" / "qlora_output"
    trainer = QLoRAFineTuner(output_dir=output_dir)
    plan = trainer.run(dataset_dir=dataset_dir, dry_run=True)

    assert plan["mode"] == "dry_run"
    assert (output_dir / "training_plan.json").exists()
