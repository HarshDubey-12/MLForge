"""Unit tests for grounded answer generation."""

from pathlib import Path

from ml_research_assistant.rag_engine.generator import GeneratorFactory
from ml_research_assistant.rag_engine.generator import AnswerGenerator


def test_generator_returns_grounded_answer_with_stub_model() -> None:
    generator = AnswerGenerator(model_name="stub-generator")
    answer = generator.generate(
        "What is attention?",
        [
            {
                "text": "Attention mechanisms help models focus on relevant tokens.",
                "metadata": {"title": "paper-a"},
                "score": 1.0,
            }
        ],
    )

    assert "attention" in answer.lower()


def test_generator_factory_falls_back_for_missing_local_checkpoint() -> None:
    model = GeneratorFactory.create(str(Path("artifacts/training/models/does-not-exist")))
    answer = model.generate(
        "What is attention?",
        [{"text": "Attention helps models focus.", "metadata": {"title": "paper-a"}}],
    )

    assert "attention" in answer.lower()
