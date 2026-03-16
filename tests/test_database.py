"""Starter unit tests for database helpers."""

from database.connection import get_engine


def test_get_engine_uses_sqlite() -> None:
    engine = get_engine()
    assert "sqlite" in str(engine.url)

