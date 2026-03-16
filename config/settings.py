"""Centralized runtime settings loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration shared across modules."""

    app_name: str = "ml_research_assistant"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    generator_model: str = "your-fine-tuned-model"
    sqlite_path: str = "./ml_research_assistant.db"
    faiss_index_path: str = "./artifacts/faiss/index.bin"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

