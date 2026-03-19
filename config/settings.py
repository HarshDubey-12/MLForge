"""Centralized runtime settings loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration shared across modules."""

    app_name: str = "ml_research_assistant"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    generator_model: str = "./artifacts/training/models/corpus_batch_001_flant5_small"
    generator_max_new_tokens: int = 192
    sqlite_path: str = "./ml_research_assistant.db"
    faiss_index_path: str = "./artifacts/faiss/index.bin"
    bm25_corpus_path: str = "./artifacts/bm25/corpus.json"
    training_dataset_dir: str = "./artifacts/training/datasets"
    training_output_dir: str = "./artifacts/training/models"
    finetune_base_model: str = "google/flan-t5-small"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
