"""Unit tests for the vector store repository."""

from pathlib import Path

from ml_research_assistant.vector_store.faiss_store import FAISSVectorStore
from ml_research_assistant.vector_store.schemas import VectorRecord


def test_vector_store_add_and_search() -> None:
    test_dir = Path("tests") / ".tmp"
    test_dir.mkdir(parents=True, exist_ok=True)
    index_path = test_dir / "vector_basic.index"
    records_path = test_dir / "vector_basic.records.json"
    for path in (index_path, records_path):
        if path.exists():
            path.unlink()

    store = FAISSVectorStore(index_path=index_path, records_path=records_path)
    store.add([[0.1] * 64], [VectorRecord(chunk_id="1", text="hello world")])
    results = store.search([0.1] * 64)
    assert len(results) == 1

    for path in (index_path, records_path):
        if path.exists():
            path.unlink()


def test_vector_store_persists_records_to_disk() -> None:
    test_dir = Path("tests") / ".tmp"
    test_dir.mkdir(parents=True, exist_ok=True)
    index_path = test_dir / "vector_test.index"
    records_path = test_dir / "vector_test.records.json"
    for path in (index_path, records_path):
        if path.exists():
            path.unlink()

    store = FAISSVectorStore(index_path=index_path, records_path=records_path)
    store.add([[0.2] * 64], [VectorRecord(chunk_id="persisted", text="stored text")])

    reloaded = FAISSVectorStore(index_path=index_path, records_path=records_path)
    results = reloaded.search([0.2] * 64)
    assert len(results) == 1
    assert results[0].chunk_id == "persisted"

    for path in (index_path, records_path):
        if path.exists():
            path.unlink()
