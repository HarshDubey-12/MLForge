"""Application factory for the FastAPI service."""

from fastapi import FastAPI

from backend.routes import conversation, health, query, upload_documents


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="ml_research_assistant")
    app.include_router(health.router)
    app.include_router(query.router)
    app.include_router(upload_documents.router)
    app.include_router(conversation.router)
    return app

