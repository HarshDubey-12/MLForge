"""Database connection and session configuration."""

from sqlalchemy import create_engine


def get_engine(sqlite_path: str = "sqlite:///ml_research_assistant.db"):
    """Return a SQLAlchemy engine for SQLite."""
    return create_engine(sqlite_path)

