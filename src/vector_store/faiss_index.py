"""
faiss_index.py

Description:
Builds and queries a FAISS vector index.
"""

import faiss
import numpy as np


class FAISSIndex:

    def __init__(self, dimension: int):

        self.index = faiss.IndexFlatIP(dimension)

    def add(self, embeddings):

        embeddings = np.asarray(
            embeddings,
            dtype=np.float32
        )

        self.index.add(embeddings)

    def search(self, query_embedding, top_k=10):

        query_embedding = np.asarray(
            [query_embedding],
            dtype=np.float32
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        return scores[0], indices[0]