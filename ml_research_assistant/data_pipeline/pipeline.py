"""Composable ingestion pipeline for document preprocessing."""

from pathlib import Path

from ml_research_assistant.data_pipeline.document_cleaner import DocumentCleaner
from ml_research_assistant.data_pipeline.metadata_extractor import MetadataExtractor
from ml_research_assistant.data_pipeline.pdf_parser import PDFParser
from ml_research_assistant.data_pipeline.semantic_chunker import SemanticChunker


class DataIngestionPipeline:
    """Pipeline Pattern implementation for the preprocessing workflow."""

    def __init__(
        self,
        parser: PDFParser,
        cleaner: DocumentCleaner,
        chunker: SemanticChunker,
        metadata_extractor: MetadataExtractor,
    ) -> None:
        self.parser = parser
        self.cleaner = cleaner
        self.chunker = chunker
        self.metadata_extractor = metadata_extractor

    def run(self, file_path: Path) -> dict[str, object]:
        """Execute the full document ingestion flow."""
        raw_text = self.parser.parse(file_path)
        cleaned_text = self.cleaner.clean(raw_text)
        chunks = self.chunker.chunk(cleaned_text)
        metadata = self.metadata_extractor.extract(cleaned_text)
        return {"chunks": chunks, "metadata": metadata}

