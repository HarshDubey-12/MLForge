# ml_research_assistant

Production-grade scaffold for a Machine Learning Research Assistant built around a fine-tuned LLM and an adaptive Retrieval-Augmented Generation (RAG) architecture.

## Architecture

- `data_pipeline`: ingestion, parsing, cleaning, chunking, metadata extraction
- `embedding`: embedding generation with SentenceTransformers
- `vector_store`: FAISS-backed indexing and repository abstractions
- `retrieval`: semantic, BM25, hybrid, and reranking strategies
- `rag_engine`: adaptive RAG pipeline components
- `training`: dataset prep, QLoRA fine-tuning, evaluation
- `backend`: FastAPI application and API routes
- `frontend`: React starter UI
- `database`: SQLite metadata access layer
- `deployment`: Docker assets and environment bootstrapping
- `config`: central configuration files
- `tests`: starter unit tests
- `scripts`: operational utility scripts

## Design Patterns

- Factory Pattern: model and retriever creation
- Strategy Pattern: interchangeable retrieval strategies
- Pipeline Pattern: orchestrated RAG execution flow
- Repository Pattern: storage access behind stable interfaces

