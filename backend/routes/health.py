"""Health endpoint for deployment monitoring."""

from fastapi import APIRouter


router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def healthcheck() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}

