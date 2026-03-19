"""Semantic chunking logic for splitting documents into retrieval units."""

import re


class SemanticChunker:
    """Chunk text into semantically meaningful passages."""

    def __init__(self, max_chars: int = 1200, min_chunk_chars: int = 250) -> None:
        self.max_chars = max_chars
        self.min_chunk_chars = min_chunk_chars

    def chunk(self, text: str) -> list[str]:
        """Split text into paragraph-aware chunks suitable for retrieval."""
        cleaned = text.strip()
        if not cleaned:
            return []

        paragraphs = self._split_paragraphs(cleaned)
        chunks: list[str] = []
        current_parts: list[str] = []
        current_length = 0

        for paragraph in paragraphs:
            paragraph_length = len(paragraph)

            if current_parts and current_length + paragraph_length + 2 > self.max_chars:
                chunks.append("\n\n".join(current_parts).strip())
                current_parts = [paragraph]
                current_length = paragraph_length
                continue

            current_parts.append(paragraph)
            current_length += paragraph_length + (2 if current_parts else 0)

        if current_parts:
            final_chunk = "\n\n".join(current_parts).strip()
            if chunks and len(final_chunk) < self.min_chunk_chars:
                chunks[-1] = f"{chunks[-1]}\n\n{final_chunk}".strip()
            else:
                chunks.append(final_chunk)

        return [chunk for chunk in chunks if chunk]

    def _split_paragraphs(self, text: str) -> list[str]:
        """Split raw text into paragraph-like blocks."""
        blocks = re.split(r"\n\s*\n+", text)
        return [self._normalize_block(block) for block in blocks if self._normalize_block(block)]

    def _normalize_block(self, block: str) -> str:
        """Normalize whitespace inside a paragraph block."""
        return re.sub(r"\s+", " ", block).strip()
