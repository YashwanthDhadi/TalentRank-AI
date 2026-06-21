"""
candidate_loader.py

Description:
    Loads candidate data from JSONL files efficiently using streaming.
"""

from pathlib import Path
from typing import Dict, Generator, List, Optional
import json


class CandidateLoader:
    """
    Loads candidate data from a JSONL file.

    Each line in the file is a valid JSON object representing one candidate.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def file_exists(self) -> bool:
        """
        Check whether the dataset file exists.
        """
        return self.file_path.exists()

    def candidate_count(self) -> int:
        """
        Count the number of candidate records.
        """
        with self.file_path.open("r", encoding="utf-8") as file:
            return sum(1 for _ in file)

    def stream_candidates(self) -> Generator[Dict, None, None]:
        """
        Yield one candidate at a time.

        This is memory efficient and suitable for very
        large datasets.
        """
        with self.file_path.open("r", encoding="utf-8") as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                yield json.loads(line)

    def load_all(self) -> List[Dict]:
        """
        Load every candidate into memory.

        Recommended only for small datasets.
        """
        return list(self.stream_candidates())

    def get_candidate_by_id(self, candidate_id: str) -> Optional[Dict]:
        """
        Find a candidate using candidate_id.
        """

        for candidate in self.stream_candidates():

            if candidate.get("candidate_id") == candidate_id:
                return candidate

        return None

    def first_candidate(self) -> Dict:
        """
        Return the first candidate.
        """

        generator = self.stream_candidates()

        return next(generator)

    def last_candidate(self) -> Dict:
        """
        Return the last candidate.
        """

        last = None

        for candidate in self.stream_candidates():
            last = candidate

        return last

    def get_candidates_batch(
        self,
        batch_size: int
    ) -> Generator[List[Dict], None, None]:
        """
        Yield candidates in batches.
        """

        batch = []

        for candidate in self.stream_candidates():

            batch.append(candidate)

            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:
            yield batch