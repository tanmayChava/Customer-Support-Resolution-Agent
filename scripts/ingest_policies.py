"""Ingest refund and resolution policies into PostgreSQL.

Planned responsibilities:
- Read policy source documents.
- Store structured policy metadata and effective dates.
- Split documents into citable chunks.
- Optionally generate embeddings for pgvector-backed retrieval.
"""
