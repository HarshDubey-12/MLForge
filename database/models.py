"""ORM models for document metadata and chunk mappings."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Document(Base):
    """Stores top-level ingested document metadata."""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    source_type = Column(String, nullable=False)


class Chunk(Base):
    """Maps text chunks back to their source documents."""

    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    chunk_ref = Column(String, nullable=False)

