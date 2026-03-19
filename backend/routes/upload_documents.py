"""Document upload endpoint for ingestion workflows."""

from fastapi import APIRouter, Depends, File, UploadFile

from backend.dependencies import (
    get_data_ingestion_pipeline,
    get_embedding_service,
    get_keyword_retriever,
    get_metadata_repository,
    get_vector_store,
)
from backend.schemas import UploadDocumentResponse
from backend.services.document_ingestion import DocumentIngestionService
from database.repository import MetadataRepository
from ml_research_assistant.data_pipeline.pipeline import DataIngestionPipeline
from ml_research_assistant.embedding.service import EmbeddingService
from ml_research_assistant.retrieval.bm25_retriever import BM25Retriever
from ml_research_assistant.vector_store.faiss_store import FAISSVectorStore


router = APIRouter(prefix="/upload_documents", tags=["documents"])


def get_document_ingestion_service(
    pipeline: DataIngestionPipeline = Depends(get_data_ingestion_pipeline),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_store: FAISSVectorStore = Depends(get_vector_store),
    keyword_retriever: BM25Retriever = Depends(get_keyword_retriever),
    metadata_repository: MetadataRepository = Depends(get_metadata_repository),
) -> DocumentIngestionService:
    """Provide the upload service instance."""
    return DocumentIngestionService(
        pipeline=pipeline,
        embedding_service=embedding_service,
        vector_store=vector_store,
        keyword_retriever=keyword_retriever,
        metadata_repository=metadata_repository,
    )


@router.post("", response_model=UploadDocumentResponse)
async def upload_documents(
    file: UploadFile = File(...),
    service: DocumentIngestionService = Depends(get_document_ingestion_service),
) -> UploadDocumentResponse:
    """Accept a document, validate it, store it locally, and run ingestion."""
    return await service.save_upload(file)
