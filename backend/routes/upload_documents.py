"""Document upload endpoint for ingestion workflows."""

from fastapi import APIRouter, UploadFile


router = APIRouter(prefix="/upload_documents", tags=["documents"])


@router.post("")
async def upload_documents(file: UploadFile) -> dict[str, str]:
    """Accept a document for downstream ingestion."""
    return {"filename": file.filename, "status": "accepted"}

