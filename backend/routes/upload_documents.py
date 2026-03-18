"""Document upload endpoint for ingestion workflows."""

from fastapi import APIRouter, Depends, File, UploadFile

from backend.dependencies import get_data_ingestion_pipeline
from backend.schemas import UploadDocumentResponse
from backend.services.document_ingestion import DocumentIngestionService
from ml_research_assistant.data_pipeline.pipeline import DataIngestionPipeline


router = APIRouter(prefix="/upload_documents", tags=["documents"])


def get_document_ingestion_service(
    pipeline: DataIngestionPipeline = Depends(get_data_ingestion_pipeline),
) -> DocumentIngestionService:
    """Provide the upload service instance."""
    return DocumentIngestionService(pipeline=pipeline)


@router.post("", response_model=UploadDocumentResponse)
async def upload_documents(
    file: UploadFile = File(...),
    service: DocumentIngestionService = Depends(get_document_ingestion_service),
) -> UploadDocumentResponse:
    """Accept a document, validate it, store it locally, and run ingestion."""
    return await service.save_upload(file)
