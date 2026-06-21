"""
candidate_retriever.py

Loads the saved FAISS index and retrieves
the most semantically similar candidates.
"""

import pickle
import faiss

from src.embeddings.embedding_engine import EmbeddingEngine


class CandidateRetriever:

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

    def retrieve(self, jd_document, top_k=1000):

        query_embedding = self.engine.encode(jd_document)

        scores, indices = self.index.search(
            query_embedding.reshape(1, -1),
            top_k
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            results.append({

                "candidate_id":
                    self.candidate_ids[idx],

                "semantic_score":
                    float(score)

            })

        return results