"""Starter unit tests for the data pipeline."""

from pathlib import Path

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

    result = pipeline.run(Path("paper.pdf"))

    assert "chunks" in result
    assert "metadata" in result

