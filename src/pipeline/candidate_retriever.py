"""Retrieve semantically similar candidates from the cached FAISS index."""

from __future__ import annotations

from src.config import DEFAULT_CANDIDATE_RETRIEVER_TOP_K
from src.embeddings.embedding_engine import EmbeddingEngine
from src.vector_store.faiss_manager import FAISSManager


class CandidateRetriever:
    """Backward-compatible wrapper around the shared FAISS manager."""

    def __init__(self):
        self.engine = EmbeddingEngine()
        self.manager = FAISSManager()
        self.index = self.manager.index
        self.candidate_ids = self.manager.candidate_ids

    def retrieve(
        self,
        jd_document: str,
        top_k: int = DEFAULT_CANDIDATE_RETRIEVER_TOP_K,
    ) -> list[dict[str, float | str]]:
        """Retrieve candidates for a job-description document."""
        query_embedding = self.engine.encode(jd_document)
        return self.manager.search_by_embedding(
            query_embedding,
            top_k=top_k,
            round_scores=False,
        )
