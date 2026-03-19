"""Starter script for QLoRA-based fine-tuning."""

from __future__ import annotations

import json
from pathlib import Path

from config.settings import settings


class QLoRAFineTuner:
    """Coordinate parameter-efficient fine-tuning of the base LLM."""

    def __init__(
        self,
        base_model_name: str | None = None,
        output_dir: str | Path | None = None,
    ) -> None:
        self.base_model_name = base_model_name or settings.finetune_base_model
        self.output_dir = Path(output_dir or settings.training_output_dir)

    def run(
        self,
        dataset_dir: str | Path,
        dry_run: bool = True,
    ) -> dict[str, object]:
        """Launch the fine-tuning workflow or emit a training plan."""
        dataset_dir = Path(dataset_dir)
        train_path = dataset_dir / "train.jsonl"
        validation_path = dataset_dir / "validation.jsonl"
        if not train_path.exists() or not validation_path.exists():
            raise FileNotFoundError("Training dataset files were not found.")

        self.output_dir.mkdir(parents=True, exist_ok=True)

        if dry_run:
            plan = {
                "mode": "dry_run",
                "base_model": self.base_model_name,
                "train_path": str(train_path),
                "validation_path": str(validation_path),
                "output_dir": str(self.output_dir),
                "strategy": "qlora_ready",
            }
            (self.output_dir / "training_plan.json").write_text(
                json.dumps(plan, indent=2),
                encoding="utf-8",
            )
            return plan

        return self._run_training(train_path=train_path, validation_path=validation_path)

    def _run_training(self, train_path: Path, validation_path: Path) -> dict[str, object]:
        """Run a practical HF fine-tuning baseline with LoRA/QLoRA-capable setup."""
        from datasets import load_dataset
        from peft import LoraConfig, get_peft_model
        from transformers import (
            AutoModelForSeq2SeqLM,
            AutoTokenizer,
            DataCollatorForSeq2Seq,
            Seq2SeqTrainer,
            Seq2SeqTrainingArguments,
        )

        dataset = load_dataset(
            "json",
            data_files={
                "train": str(train_path),
                "validation": str(validation_path),
            },
        )

        tokenizer = AutoTokenizer.from_pretrained(self.base_model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.base_model_name)
        lora_config = LoraConfig(
            r=8,
            lora_alpha=16,
            lora_dropout=0.05,
            target_modules=["q", "v"],
            task_type="SEQ_2_SEQ_LM",
        )
        model = get_peft_model(model, lora_config)

        def preprocess(batch: dict[str, list[str]]) -> dict[str, object]:
            inputs = [
                f"Instruction: {instruction}\nInput: {input_text}\nAnswer:"
                for instruction, input_text in zip(batch["instruction"], batch["input"])
            ]
            model_inputs = tokenizer(inputs, truncation=True, max_length=768)
            labels = tokenizer(
                batch["output"],
                truncation=True,
                max_length=256,
            )
            model_inputs["labels"] = labels["input_ids"]
            return model_inputs

        tokenized_dataset = dataset.map(preprocess, batched=True)
        training_args = Seq2SeqTrainingArguments(
            output_dir=str(self.output_dir),
            per_device_train_batch_size=1,
            per_device_eval_batch_size=1,
            learning_rate=2e-4,
            num_train_epochs=1,
            logging_steps=5,
            eval_strategy="epoch",
            save_strategy="epoch",
            predict_with_generate=True,
            fp16=False,
            use_cpu=True,
            report_to=[],
        )

        trainer = Seq2SeqTrainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset["train"],
            eval_dataset=tokenized_dataset["validation"],
            tokenizer=tokenizer,
            data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model),
        )

        trainer.train()
        trainer.save_model(str(self.output_dir))
        tokenizer.save_pretrained(str(self.output_dir))

        manifest = {
            "mode": "trained",
            "base_model": self.base_model_name,
            "output_dir": str(self.output_dir),
        }
        (self.output_dir / "training_manifest.json").write_text(
            json.dumps(manifest, indent=2),
            encoding="utf-8",
        )
        return manifest
