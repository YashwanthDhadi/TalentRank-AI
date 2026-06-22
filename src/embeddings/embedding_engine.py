"""Generate dense vector embeddings using Sentence Transformers."""

from __future__ import annotations

from typing import Sequence

import numpy as np
from sentence_transformers import SentenceTransformer

from src.config import EMBEDDING_MODEL_NAME


class EmbeddingEngine:
    """Generate normalized float32 embeddings."""

    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str) -> np.ndarray:
        """Encode a single text string."""
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text to encode must be a non-empty string.")
        embedding = self.model.encode(text, normalize_embeddings=True)
        return np.asarray(embedding, dtype=np.float32)

    def encode_batch(self, texts: Sequence[str]) -> np.ndarray:
        """Encode a batch of text strings."""
        if not texts:
            raise ValueError("Batch to encode must contain at least one text.")
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        return np.asarray(embeddings, dtype=np.float32)
