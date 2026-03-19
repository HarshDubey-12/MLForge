"""Application factory for the FastAPI service."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import conversation, health, query, upload_documents


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="ml_research_assistant")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:3000",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
            "http://localhost:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    app.include_router(query.router)
    app.include_router(upload_documents.router)
    app.include_router(conversation.router)
    return app
