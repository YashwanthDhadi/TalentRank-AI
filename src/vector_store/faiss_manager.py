"""Load the cached FAISS index and retrieve candidates."""

from __future__ import annotations

from time import perf_counter
from typing import Any

import faiss
import numpy as np

from src.config import CANDIDATE_IDS_PATH, DEFAULT_RETRIEVAL_TOP_K, FAISS_INDEX_PATH
from src.embeddings.embedding_engine import EmbeddingEngine
from src.utils.artifact_utils import get_logger, load_pickle


class FAISSManager:
    """Load and query the production FAISS index."""

    def __init__(
        self,
        index_path: str = str(FAISS_INDEX_PATH),
        candidate_ids_path: str = str(CANDIDATE_IDS_PATH),
    ):
        self.logger = get_logger(__name__)
        self.engine = EmbeddingEngine()

        load_start = perf_counter()
        try:
            self.index = faiss.read_index(index_path)
        except RuntimeError as exc:
            raise ValueError(
                f"The FAISS index at '{index_path}' is missing or corrupted."
            ) from exc

        self.candidate_ids = load_pickle(candidate_ids_path, "candidate id cache")

        if self.index.ntotal <= 0:
            raise ValueError(f"The FAISS index at '{index_path}' is empty.")
        if not isinstance(self.candidate_ids, list) or not self.candidate_ids:
            raise ValueError(
                f"The candidate id cache at '{candidate_ids_path}' is empty or invalid."
            )
        if len(self.candidate_ids) != self.index.ntotal:
            raise ValueError(
                "FAISS index size does not match the number of cached candidate ids: "
                f"{self.index.ntotal} != {len(self.candidate_ids)}."
            )

        self.logger.info(
            "FAISS loading time: %.3fs for %s vectors",
            perf_counter() - load_start,
            self.index.ntotal,
        )

    def search(
        self,
        text: str,
        top_k: int = DEFAULT_RETRIEVAL_TOP_K,
    ) -> list[dict[str, Any]]:
        """Encode query text and search the FAISS index."""
        embedding = self.engine.encode(text)
        return self.search_by_embedding(embedding, top_k=top_k, round_scores=True)

    def search_by_embedding(
        self,
        embedding: np.ndarray,
        top_k: int,
        round_scores: bool,
    ) -> list[dict[str, Any]]:
        """Search the FAISS index using a precomputed embedding."""
        if top_k <= 0:
            raise ValueError("top_k must be a positive integer.")

        query_top_k = min(top_k, self.index.ntotal)
        query_embedding = np.asarray(embedding, dtype=np.float32).reshape(1, -1)
        scores, indices = self.index.search(query_embedding, query_top_k)

        results: list[dict[str, Any]] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            semantic_score = float(score)
            if round_scores:
                semantic_score = round(semantic_score, 4)
            results.append(
                {
                    "candidate_id": self.candidate_ids[idx],
                    "semantic_score": semantic_score,
                }
            )

        return results
