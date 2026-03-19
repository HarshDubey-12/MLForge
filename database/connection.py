"""Database connection and session configuration."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config.settings import settings
from database.models import Base


def _normalize_sqlite_url(sqlite_path: str) -> str:
    """Normalize filesystem paths into SQLAlchemy SQLite URLs."""
    if sqlite_path.startswith("sqlite:///"):
        return sqlite_path
    return f"sqlite:///{sqlite_path}"


def get_engine(sqlite_path: str | None = None):
    """Return a SQLAlchemy engine for SQLite."""
    normalized_path = _normalize_sqlite_url(sqlite_path or settings.sqlite_path)
    return create_engine(normalized_path, future=True)


def get_session_factory(sqlite_path: str | None = None) -> sessionmaker[Session]:
    """Return a configured SQLAlchemy session factory."""
    engine = get_engine(sqlite_path=sqlite_path)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def initialize_database(sqlite_path: str | None = None) -> None:
    """Create database tables if they do not already exist."""
    engine = get_engine(sqlite_path=sqlite_path)
    Base.metadata.create_all(engine)
