"""Metadata extraction for document title, authors, source, and tags."""

import re


class MetadataExtractor:
    """Extract structured metadata from ingested documents."""

    def extract(self, text: str) -> dict[str, str]:
        """Derive lightweight metadata from document content."""
        cleaned = text.strip()
        if not cleaned:
            return {
                "title": "unknown",
                "source_type": "empty",
                "word_count": "0",
                "document_style": "unknown",
            }

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        title = self._infer_title(lines)
        source_type = self._infer_source_type(text)
        word_count = str(len(re.findall(r"\b\w+\b", text)))
        document_style = self._infer_document_style(text)

        return {
            "title": title,
            "source_type": source_type,
            "word_count": word_count,
            "document_style": document_style,
        }

    def _infer_title(self, lines: list[str]) -> str:
        """Infer a likely document title from the opening non-empty lines."""
        for line in lines[:5]:
            normalized = re.sub(r"\s+", " ", line).strip()
            if len(normalized) >= 10:
                return normalized[:160]
        return "unknown"

    def _infer_source_type(self, text: str) -> str:
        """Guess the source type based on common textual cues."""
        lowered = text.lower()

        if "abstract" in lowered and "introduction" in lowered:
            return "research_paper"
        if "chapter" in lowered:
            return "book_or_longform"
        if "references" in lowered or "bibliography" in lowered:
            return "academic_document"
        return "general_document"

    def _infer_document_style(self, text: str) -> str:
        """Classify whether the writing looks academic or general."""
        lowered = text.lower()
        academic_markers = ["abstract", "method", "results", "discussion", "references"]

        matches = sum(1 for marker in academic_markers if marker in lowered)
        if matches >= 2:
            return "academic"
        return "general"
