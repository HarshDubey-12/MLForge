"""PDF parsing utilities for extracting raw text from research documents."""

from pathlib import Path

from pypdf import PdfReader


class PDFParser:
    """Parse research documents into raw textual content."""

    def parse(self, file_path: Path) -> str:
        """Extract text from a supported document path."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            return self._parse_pdf(file_path)

        if suffix in {".txt", ".md"}:
            return file_path.read_text(encoding="utf-8", errors="ignore")

        raise ValueError(f"Unsupported file type for parsing: {suffix}")

    def _parse_pdf(self, file_path: Path) -> str:
        """Extract text from a PDF document using pypdf."""
        reader = PdfReader(str(file_path))
        pages = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(page.strip() for page in pages if page.strip())
        return text.strip()
