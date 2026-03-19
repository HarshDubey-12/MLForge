"""Unit tests for database helpers and repositories."""

from pathlib import Path
from uuid import uuid4

from database.connection import get_engine, get_session_factory, initialize_database
from database.repository import MetadataRepository


def test_get_engine_uses_sqlite() -> None:
    engine = get_engine()
    assert "sqlite" in str(engine.url)


def test_metadata_repository_saves_document_and_chunks() -> None:
    db_path = Path("tests") / ".tmp" / f"metadata_repository_{uuid4().hex}.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    sqlite_url = f"sqlite:///{db_path}"
    initialize_database(sqlite_path=sqlite_url)
    repository = MetadataRepository(get_session_factory(sqlite_path=sqlite_url))

    document, chunks = repository.save_document(
        source_filename="paper.txt",
        stored_filename="stored_paper.txt",
        stored_path="uploads/stored_paper.txt",
        content_type="text/plain",
        size_bytes=42,
        metadata={
            "title": "Attention Is All You Need",
            "source_type": "research_paper",
            "document_style": "academic",
            "word_count": "7",
        },
        chunks=["chunk one", "chunk two"],
    )

    assert document.id is not None
    assert len(chunks) == 2
    assert repository.get_keyword_documents()
