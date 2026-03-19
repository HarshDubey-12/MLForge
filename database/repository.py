"""Repository objects for document and chunk metadata."""

from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy.orm import Session, sessionmaker

from database.models import Chunk, Document
from ml_research_assistant.vector_store.schemas import VectorRecord


class MetadataRepository:
    """Coordinate persistence of document and chunk metadata."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def save_document(
        self,
        *,
        source_filename: str,
        stored_filename: str,
        stored_path: str,
        content_type: str,
        size_bytes: int,
        metadata: dict[str, str],
        chunks: Sequence[str],
    ) -> tuple[Document, list[Chunk]]:
        """Persist a document and its chunks."""
        document = Document(
            source_filename=source_filename,
            stored_filename=stored_filename,
            stored_path=stored_path,
            content_type=content_type,
            size_bytes=size_bytes,
            title=metadata.get("title", "unknown"),
            source_type=metadata.get("source_type", "general_document"),
            document_style=metadata.get("document_style", "general"),
            word_count=int(metadata.get("word_count", "0") or 0),
            metadata_json=metadata,
        )

        with self.session_factory() as session:
            session.add(document)
            session.flush()

            chunk_rows = [
                Chunk(
                    document_id=document.id,
                    chunk_ref=f"{stored_filename}:{index}",
                    text=chunk_text,
                    metadata_json={**metadata, "source_filename": source_filename},
                )
                for index, chunk_text in enumerate(chunks)
            ]

            session.add_all(chunk_rows)
            session.commit()

            session.refresh(document)
            for chunk in chunk_rows:
                session.refresh(chunk)

            return document, chunk_rows

    def get_all_chunks(self) -> list[Chunk]:
        """Return all stored chunks."""
        with self.session_factory() as session:
            return session.query(Chunk).order_by(Chunk.id.asc()).all()

    def get_keyword_documents(self) -> list[dict[str, object]]:
        """Return chunk documents for keyword retrieval indexing."""
        return [
            {
                "chunk_id": chunk.chunk_ref,
                "text": chunk.text,
                "metadata": chunk.metadata_json,
            }
            for chunk in self.get_all_chunks()
        ]

    def get_vector_records(self) -> list[VectorRecord]:
        """Return all chunks as vector-store records."""
        return [
            VectorRecord(
                chunk_id=chunk.chunk_ref,
                text=chunk.text,
                metadata=chunk.metadata_json,
            )
            for chunk in self.get_all_chunks()
        ]
