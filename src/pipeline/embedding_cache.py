"""
embedding_cache.py

Build candidate embeddings in batches and save:
1. candidate_embeddings.npy
2. candidate_ids.pkl
3. faiss.index
"""

import os
import pickle
import numpy as np
import faiss

from src.data_loader.candidate_loader import CandidateLoader
from src.preprocessing.candidate_parser import CandidateParser
from src.feature_engineering.candidate_document import CandidateDocument
from src.embeddings.embedding_engine import EmbeddingEngine


class EmbeddingCache:

    def __init__(
        self,
        dataset_path="data/raw/candidates.jsonl",
        output_dir="artifacts",
        batch_size=128
    ):

        self.loader = CandidateLoader(dataset_path)
        self.engine = EmbeddingEngine()

        self.output_dir = output_dir
        self.batch_size = batch_size

        os.makedirs(output_dir, exist_ok=True)

    def build(self, limit=None):

        documents = []
        candidate_ids = []
        embeddings = []

        total = 0

        print("=" * 60)
        print("Building Candidate Embedding Cache")
        print("=" * 60)

        for candidate in self.loader.stream_candidates():

            parsed = CandidateParser.parse(candidate)

            doc = CandidateDocument.build(parsed)

            documents.append(doc)

            candidate_ids.append(parsed["candidate_id"])

            total += 1

            if len(documents) == self.batch_size:

                batch_embeddings = self.engine.encode_batch(documents)

                embeddings.extend(batch_embeddings)

                print(f"Processed : {total}")

                documents = []

            if limit is not None and total >= limit:
                break

        if documents:

            batch_embeddings = self.engine.encode_batch(documents)

            embeddings.extend(batch_embeddings)

        embeddings = np.asarray(
            embeddings,
            dtype=np.float32
        )

        np.save(
            os.path.join(
                self.output_dir,
                "candidate_embeddings.npy"
            ),
            embeddings
        )

        with open(
            os.path.join(
                self.output_dir,
                "candidate_ids.pkl"
            ),
            "wb"
        ) as f:

            pickle.dump(candidate_ids, f)

        index = faiss.IndexFlatIP(
            embeddings.shape[1]
        )

        index.add(embeddings)

        faiss.write_index(
            index,
            os.path.join(
                self.output_dir,
                "faiss.index"
            )
        )

        print()

        print("=" * 60)
        print("CACHE BUILD COMPLETED")
        print("=" * 60)
        print("Candidates :", len(candidate_ids))
        print("Embeddings :", embeddings.shape)
        print("FAISS Index :", index.ntotal)