"""Service layer for document upload and ingestion preparation."""

from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from backend.schemas import UploadDocumentResponse
from ml_research_assistant.data_pipeline.pipeline import DataIngestionPipeline


UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}


class DocumentIngestionService:
    """Handle upload validation, local file persistence, and ingestion preparation."""

    def __init__(
        self,
        pipeline: DataIngestionPipeline,
        upload_dir: Path | None = None,
    ) -> None:
        self.pipeline = pipeline
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

        return UploadDocumentResponse(
            filename=file.filename,
            stored_filename=safe_name,
            stored_path=str(file_path),
            content_type=file.content_type or "unknown",
            size_bytes=len(content),
            status="accepted",
            ingestion_status="processed",
            chunk_count=len(chunks),
            metadata=metadata,
        )
