"""Build candidate embeddings, lookup cache, and FAISS index artifacts."""

from __future__ import annotations

import pickle
from pathlib import Path
from time import perf_counter
from typing import Any

import faiss
import numpy as np
from numpy.lib.format import open_memmap

from src.config import (
    ARTIFACTS_DIR,
    CANDIDATE_IDS_PATH,
    CANDIDATE_LOOKUP_PATH,
    DATASET_PATH,
    EMBEDDING_BATCH_SIZE,
    EMBEDDINGS_PATH,
    FAISS_INDEX_PATH,
    LOG_PROGRESS_EVERY_BATCHES,
)
from src.data_loader.candidate_loader import CandidateLoader
from src.embeddings.embedding_engine import EmbeddingEngine
from src.feature_engineering.candidate_document import CandidateDocument
from src.preprocessing.candidate_parser import CandidateParser
from src.utils.artifact_utils import (
    create_temp_path,
    ensure_directory,
    file_size_bytes,
    get_logger,
    replace_file,
)


class EmbeddingCache:
    """Build production embedding and lookup artifacts for the full dataset."""

    def __init__(
        self,
        dataset_path: str = str(DATASET_PATH),
        output_dir: str = str(ARTIFACTS_DIR),
        batch_size: int = EMBEDDING_BATCH_SIZE,
    ):
        if batch_size <= 0:
            raise ValueError("Batch size must be a positive integer.")

        self.loader = CandidateLoader(dataset_path)
        self.engine = EmbeddingEngine()
        self.output_dir = ensure_directory(Path(output_dir))
        self.batch_size = batch_size
        self.logger = get_logger(__name__)

        self.embeddings_path = self.output_dir / EMBEDDINGS_PATH.name
        self.candidate_ids_path = self.output_dir / CANDIDATE_IDS_PATH.name
        self.candidate_lookup_path = self.output_dir / CANDIDATE_LOOKUP_PATH.name
        self.faiss_index_path = self.output_dir / FAISS_INDEX_PATH.name

    def build(self, limit: int | None = None) -> dict[str, Any]:
        """Build embeddings, candidate lookup cache, and FAISS index safely."""
        if limit is not None and limit <= 0:
            raise ValueError("limit must be a positive integer when provided.")

        dataset_count = self.loader.candidate_count()
        target_count = min(dataset_count, limit) if limit is not None else dataset_count
        if target_count == 0:
            raise ValueError("Candidate dataset is empty. No embedding cache can be built.")

        self.logger.info("Building candidate embedding cache for %s candidates", target_count)

        build_start = perf_counter()
        embedding_start = perf_counter()
        processed = 0
        batch_number = 0
        candidate_ids: list[str] = []
        candidate_lookup: dict[str, dict[str, Any]] = {}
        index: faiss.IndexFlatIP | None = None
        embeddings_memmap = None
        temp_paths: list[Path] = []

        try:
            embeddings_temp_path = create_temp_path(self.embeddings_path)
            candidate_ids_temp_path = create_temp_path(self.candidate_ids_path)
            candidate_lookup_temp_path = create_temp_path(self.candidate_lookup_path)
            faiss_temp_path = create_temp_path(self.faiss_index_path)
            temp_paths.extend(
                [
                    embeddings_temp_path,
                    candidate_ids_temp_path,
                    candidate_lookup_temp_path,
                    faiss_temp_path,
                ]
            )

            for raw_batch in self.loader.get_candidates_batch(self.batch_size):
                remaining = target_count - processed
                if remaining <= 0:
                    break

                current_batch = raw_batch[:remaining]
                documents: list[str] = []

                for candidate in current_batch:
                    parsed_candidate = CandidateParser.parse(candidate)
                    candidate_id = parsed_candidate.get("candidate_id")

                    if not candidate_id:
                        raise ValueError("Candidate record is missing 'candidate_id'.")
                    if candidate_id in candidate_lookup:
                        raise ValueError(
                            f"Duplicate candidate_id '{candidate_id}' found in dataset."
                        )

                    candidate_lookup[candidate_id] = parsed_candidate
                    candidate_ids.append(candidate_id)
                    documents.append(CandidateDocument.build(parsed_candidate))

                batch_embeddings = self.engine.encode_batch(documents)

                if index is None:
                    dimension = int(batch_embeddings.shape[1])
                    embeddings_memmap = open_memmap(
                        embeddings_temp_path,
                        mode="w+",
                        dtype=np.float32,
                        shape=(target_count, dimension),
                    )
                    index = faiss.IndexFlatIP(dimension)

                batch_size = len(documents)
                start_index = processed
                end_index = processed + batch_size
                embeddings_memmap[start_index:end_index] = batch_embeddings
                index.add(batch_embeddings)

                processed = end_index
                batch_number += 1

                if (
                    batch_number % LOG_PROGRESS_EVERY_BATCHES == 0
                    or processed == target_count
                ):
                    self.logger.info(
                        "Embedding progress: %s/%s candidates processed",
                        processed,
                        target_count,
                    )

            if index is None or embeddings_memmap is None:
                raise ValueError("No embeddings were generated from the candidate dataset.")
            if processed != target_count:
                raise ValueError(
                    f"Embedding build processed {processed} candidates, expected {target_count}."
                )

            embedding_generation_time = perf_counter() - embedding_start

            embeddings_memmap.flush()
            del embeddings_memmap
            embeddings_memmap = None

            with candidate_ids_temp_path.open("wb") as candidate_ids_file:
                pickle.dump(
                    candidate_ids,
                    candidate_ids_file,
                    protocol=pickle.HIGHEST_PROTOCOL,
                )

            with candidate_lookup_temp_path.open("wb") as candidate_lookup_file:
                pickle.dump(
                    candidate_lookup,
                    candidate_lookup_file,
                    protocol=pickle.HIGHEST_PROTOCOL,
                )

            faiss.write_index(index, str(faiss_temp_path))

            if index.ntotal != target_count:
                raise ValueError(
                    f"FAISS index contains {index.ntotal} vectors, expected {target_count}."
                )
            if file_size_bytes(faiss_temp_path) <= 0:
                raise ValueError("Generated FAISS index artifact is empty.")

            replace_file(embeddings_temp_path, self.embeddings_path)
            replace_file(candidate_ids_temp_path, self.candidate_ids_path)
            replace_file(candidate_lookup_temp_path, self.candidate_lookup_path)
            replace_file(faiss_temp_path, self.faiss_index_path)

            final_index = faiss.read_index(str(self.faiss_index_path))
            if final_index.ntotal != target_count:
                raise ValueError(
                    "Final FAISS index verification failed: "
                    f"{final_index.ntotal} != {target_count}."
                )

            total_execution_time = perf_counter() - build_start
            faiss_index_size_bytes = file_size_bytes(self.faiss_index_path)

            self.logger.info("Embedding generation time: %.3fs", embedding_generation_time)
            self.logger.info(
                "FAISS index verification complete: %s vectors, %.2f MB",
                final_index.ntotal,
                faiss_index_size_bytes / (1024 * 1024),
            )
            self.logger.info("Total cache build time: %.3fs", total_execution_time)

            return {
                "candidate_count": target_count,
                "embedding_shape": (target_count, final_index.d),
                "faiss_index_size_bytes": faiss_index_size_bytes,
                "embedding_generation_time": embedding_generation_time,
                "total_execution_time": total_execution_time,
            }
        finally:
            if embeddings_memmap is not None:
                del embeddings_memmap
            for temp_path in temp_paths:
                if temp_path.exists():
                    temp_path.unlink()
