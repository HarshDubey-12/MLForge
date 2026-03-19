"""Service layer for document upload and ingestion preparation."""

from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from backend.schemas import UploadDocumentResponse
from database.repository import MetadataRepository
from ml_research_assistant.data_pipeline.pipeline import DataIngestionPipeline
from ml_research_assistant.embedding.service import EmbeddingService
from ml_research_assistant.retrieval.bm25_retriever import BM25Retriever
from ml_research_assistant.vector_store.faiss_store import FAISSVectorStore
from ml_research_assistant.vector_store.schemas import VectorRecord


UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}


class DocumentIngestionService:
    """Handle upload validation, local file persistence, and ingestion preparation."""

    def __init__(
        self,
        pipeline: DataIngestionPipeline,
        embedding_service: EmbeddingService,
        vector_store: FAISSVectorStore,
        keyword_retriever: BM25Retriever,
        metadata_repository: MetadataRepository,
        upload_dir: Path | None = None,
    ) -> None:
        self.pipeline = pipeline
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.keyword_retriever = keyword_retriever
        self.metadata_repository = metadata_repository
        self.upload_dir = upload_dir or UPLOAD_DIR

    async def save_upload(self, file: UploadFile) -> UploadDocumentResponse:
        """Validate an uploaded file, persist it locally, and run ingestion."""
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file must have a filename.",
            )

        extension = Path(file.filename).suffix.lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Unsupported file type: {extension}. Allowed types are: "
                    f"{', '.join(sorted(ALLOWED_EXTENSIONS))}."
                ),
            )

        content = await file.read()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty.",
            )

        self.upload_dir.mkdir(parents=True, exist_ok=True)

        safe_name = f"{uuid4().hex}_{Path(file.filename).name}"
        file_path = self.upload_dir / safe_name
        file_path.write_bytes(content)

        ingestion_result = self.pipeline.run(file_path)
        chunks = ingestion_result.get("chunks", [])
        metadata = ingestion_result.get("metadata", {})

        document, chunk_rows = self.metadata_repository.save_document(
            source_filename=file.filename,
            stored_filename=safe_name,
            stored_path=str(file_path),
            content_type=file.content_type or "unknown",
            size_bytes=len(content),
            metadata=metadata,
            chunks=chunks,
        )

        if chunks:
            embeddings = self.embedding_service.embed_documents(chunks)
            records = [
                VectorRecord(
                    chunk_id=chunk.chunk_ref,
                    text=chunk.text,
                    metadata=chunk.metadata_json,
                )
                for chunk in chunk_rows
            ]
            self.vector_store.add(embeddings, records)
            self.keyword_retriever.index(self.metadata_repository.get_keyword_documents())

        return UploadDocumentResponse(
            filename=file.filename,
            stored_filename=safe_name,
            stored_path=str(file_path),
            content_type=file.content_type or "unknown",
            size_bytes=len(content),
            status=f"accepted_document_{document.id}",
            ingestion_status="processed",
            chunk_count=len(chunks),
            metadata=metadata,
        )
