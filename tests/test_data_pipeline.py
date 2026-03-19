"""Starter unit tests for the data pipeline."""

from pathlib import Path
from uuid import uuid4

from ml_research_assistant.data_pipeline.document_cleaner import DocumentCleaner
from ml_research_assistant.data_pipeline.metadata_extractor import MetadataExtractor
from ml_research_assistant.data_pipeline.pdf_parser import PDFParser
from ml_research_assistant.data_pipeline.pipeline import DataIngestionPipeline
from ml_research_assistant.data_pipeline.semantic_chunker import SemanticChunker


def test_data_ingestion_pipeline_returns_chunks_and_metadata() -> None:
    pipeline = DataIngestionPipeline(
        parser=PDFParser(),
        cleaner=DocumentCleaner(),
        chunker=SemanticChunker(),
        metadata_extractor=MetadataExtractor(),
    )

    test_dir = Path("tests") / ".tmp"
    test_dir.mkdir(parents=True, exist_ok=True)
    file_path = test_dir / f"paper_{uuid4().hex}.txt"

    try:
        file_path.write_text(
            "Attention Is All You Need\n\nAbstract\nTransformers rely on self attention.",
            encoding="utf-8",
        )
        result = pipeline.run(file_path)
    finally:
        if file_path.exists():
            file_path.unlink()

    assert "chunks" in result
    assert result["chunks"]
    assert "metadata" in result
