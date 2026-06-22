"""Load candidate records from a JSONL dataset."""

import json
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional

from src.utils.artifact_utils import ensure_file_exists


class CandidateLoader:
    """Load candidate data from a JSONL file."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def file_exists(self) -> bool:
        """Check whether the dataset file exists."""
        return self.file_path.exists()

    def candidate_count(self) -> int:
        """Count the number of candidate records."""
        ensure_file_exists(self.file_path, "candidate dataset")
        with self.file_path.open("r", encoding="utf-8") as file:
            return sum(1 for line in file if line.strip())

    def stream_candidates(self) -> Generator[Dict[str, Any], None, None]:
        """Yield one candidate at a time."""
        ensure_file_exists(self.file_path, "candidate dataset")
        with self.file_path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        "Invalid candidate dataset JSON at "
                        f"'{self.file_path}', line {line_number}."
                    ) from exc

    def load_all(self) -> List[Dict[str, Any]]:
        """Load every candidate into memory."""
        return list(self.stream_candidates())

    def get_candidate_by_id(self, candidate_id: str) -> Optional[Dict[str, Any]]:
        """Find a candidate using candidate_id."""
        for candidate in self.stream_candidates():
            if candidate.get("candidate_id") == candidate_id:
                return candidate
        return None

    def first_candidate(self) -> Dict[str, Any]:
        """Return the first candidate."""
        generator = self.stream_candidates()
        try:
            return next(generator)
        except StopIteration as exc:
            raise ValueError(
                f"No candidates were found in dataset '{self.file_path}'."
            ) from exc

    def last_candidate(self) -> Dict[str, Any]:
        """Return the last candidate."""
        last: Optional[Dict[str, Any]] = None
        for candidate in self.stream_candidates():
            last = candidate
        if last is None:
            raise ValueError(f"No candidates were found in dataset '{self.file_path}'.")
        return last

    def get_candidates_batch(
        self,
        batch_size: int,
    ) -> Generator[List[Dict[str, Any]], None, None]:
        """Yield candidates in batches."""
        if batch_size <= 0:
            raise ValueError("Batch size must be a positive integer.")
        batch: List[Dict[str, Any]] = []
        for candidate in self.stream_candidates():
            batch.append(candidate)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
