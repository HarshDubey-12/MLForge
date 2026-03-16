"""PDF parsing utilities for extracting raw text from research documents."""

from pathlib import Path


class PDFParser:
    """Parse PDF files into raw textual content."""

    def parse(self, file_path: Path) -> str:
        """Return raw text extracted from a PDF."""
        return f"Parsed text placeholder for {file_path.name}"

