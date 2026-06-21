"""
faiss_manager.py

Loads the cached FAISS index and retrieves candidates.
"""

import pickle
import faiss

from src.embeddings.embedding_engine import EmbeddingEngine


class FAISSManager:

    def __init__(self):

        self.engine = EmbeddingEngine()

        self.index = faiss.read_index(
            "artifacts/faiss.index"
        )

        with open(
            "artifacts/candidate_ids.pkl",
            "rb"
        ) as f:

            self.candidate_ids = pickle.load(f)

    def search(self, text, top_k=10):

        embedding = self.engine.encode(text)

        scores, indices = self.index.search(
            embedding.reshape(1, -1),
            top_k
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            results.append({

                "candidate_id": self.candidate_ids[idx],

                "semantic_score": round(float(score), 4)

            })

        return results