"""LLM response generation and model loading factory hooks."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from config.settings import settings


class _FallbackGenerationModel:
    """Deterministic extractive fallback when HF generation is unavailable."""

    def generate(self, query: str, contexts: list[dict[str, object]]) -> str:
        if not contexts:
            return (
                "I could not find supporting evidence in the indexed knowledge base for "
                f"the query: {query}"
            )

        summary_points: list[str] = []
        query_terms = set(re.findall(r"\b\w+\b", query.lower()))

        for context in contexts[:3]:
            text = str(context.get("text", "")).strip()
            if not text:
                continue
            source = str(context.get("metadata", {}).get("title", "source"))
            sentence = self._extract_relevant_sentence(text, query_terms)
            summary_points.append(f"{sentence} ({source})")

        joined = " ".join(summary_points)
        return f"Based on the retrieved evidence, {joined}"

    def _extract_relevant_sentence(self, text: str, query_terms: set[str]) -> str:
        sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+", text)
            if sentence.strip()
        ]
        if not sentences:
            return text[:240]

        scored = sorted(
            sentences,
            key=lambda sentence: self._sentence_score(sentence, query_terms),
            reverse=True,
        )
        return scored[0][:240]

    def _sentence_score(self, sentence: str, query_terms: set[str]) -> tuple[int, int]:
        sentence_terms = set(re.findall(r"\b\w+\b", sentence.lower()))
        overlap = len(query_terms & sentence_terms)
        return (overlap, len(sentence))


class _HFGenerationModel:
    """Thin wrapper around a Hugging Face text generation pipeline."""

    def __init__(self, generator: Any) -> None:
        self.generator = generator

    def generate(self, query: str, contexts: list[dict[str, object]]) -> str:
        prompt = self._build_prompt(query, contexts)
        response = self.generator(
            prompt,
            max_new_tokens=settings.generator_max_new_tokens,
            do_sample=False,
        )

        if not response:
            return ""

        first = response[0]
        if "generated_text" in first:
            generated = str(first["generated_text"])
            return generated[len(prompt) :].strip() or generated.strip()
        if "summary_text" in first:
            return str(first["summary_text"]).strip()
        return str(first).strip()

    def _build_prompt(self, query: str, contexts: list[dict[str, object]]) -> str:
        context_lines = []
        for index, context in enumerate(contexts[:4], start=1):
            title = str(context.get("metadata", {}).get("title", f"context {index}"))
            text = str(context.get("text", ""))[:500]
            context_lines.append(f"[{index}] {title}: {text}")

        context_block = "\n".join(context_lines) if context_lines else "No context available."
        return (
            "You are an ML research assistant. Answer the question using only the provided "
            "context. If evidence is weak, say so.\n\n"
            f"Question: {query}\n\n"
            f"Context:\n{context_block}\n\n"
            "Answer:"
        )


class _HFSeq2SeqGenerationModel:
    """Direct model wrapper for local HF and PEFT seq2seq checkpoints."""

    def __init__(self, model: Any, tokenizer: Any) -> None:
        self.model = model
        self.tokenizer = tokenizer

    def generate(self, query: str, contexts: list[dict[str, object]]) -> str:
        prompt = self._build_prompt(query, contexts)

        try:
            import torch
        except Exception:
            return _FallbackGenerationModel().generate(query, contexts)

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=768,
        )
        self.model.to("cpu")
        self.model.eval()

        with torch.no_grad():
            generated = self.model.generate(
                **inputs,
                max_new_tokens=settings.generator_max_new_tokens,
                do_sample=False,
            )

        return self.tokenizer.decode(generated[0], skip_special_tokens=True).strip()

    def _build_prompt(self, query: str, contexts: list[dict[str, object]]) -> str:
        context_lines = []
        for index, context in enumerate(contexts[:4], start=1):
            title = str(context.get("metadata", {}).get("title", f"context {index}"))
            text = str(context.get("text", ""))[:500]
            context_lines.append(f"[{index}] {title}: {text}")

        context_block = "\n".join(context_lines) if context_lines else "No context available."
        return (
            "Instruction: Answer the question using the provided research context only.\n"
            f"Input: Question: {query}\nContext:\n{context_block}\n"
            "Answer:"
        )


class GeneratorFactory:
    """Factory Pattern for constructing generator model adapters."""

    @staticmethod
    def create(model_name: str):
        """Return a HF-backed generator when available, otherwise a fallback generator."""
        if model_name == "stub-generator":
            return _FallbackGenerationModel()

        try:
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

            local_model_path = Path(model_name)
            if local_model_path.exists() and local_model_path.is_dir():
                adapter_config_path = local_model_path / "adapter_config.json"
                if adapter_config_path.exists():
                    try:
                        from peft import PeftModel

                        adapter_config = json.loads(adapter_config_path.read_text(encoding="utf-8"))
                        base_model_name = adapter_config["base_model_name_or_path"]
                        tokenizer = AutoTokenizer.from_pretrained(str(local_model_path))
                        base_model = AutoModelForSeq2SeqLM.from_pretrained(base_model_name)
                        model = PeftModel.from_pretrained(base_model, str(local_model_path))
                        return _HFSeq2SeqGenerationModel(model=model, tokenizer=tokenizer)
                    except Exception:
                        return _FallbackGenerationModel()

                try:
                    tokenizer = AutoTokenizer.from_pretrained(str(local_model_path))
                    model = AutoModelForSeq2SeqLM.from_pretrained(str(local_model_path))
                    return _HFSeq2SeqGenerationModel(model=model, tokenizer=tokenizer)
                except Exception:
                    return _FallbackGenerationModel()

            try:
                generator = pipeline("text2text-generation", model=model_name)
            except Exception:
                generator = pipeline("text-generation", model=model_name)
            return _HFGenerationModel(generator)
        except Exception:
            return _FallbackGenerationModel()


class AnswerGenerator:
    """Generate answers grounded in retrieved research context."""

    def __init__(self, model_name: str) -> None:
        self.model = GeneratorFactory.create(model_name)

    def generate(self, query: str, contexts: list[dict[str, object]]) -> str:
        """Generate a grounded answer from retrieved contexts."""
        return self.model.generate(query, contexts)
