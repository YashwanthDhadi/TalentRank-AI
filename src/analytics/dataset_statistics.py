"""Build dataset-wide statistics for recruiter-signal normalization."""

from __future__ import annotations

from src.config import DATASET_PATH, DATASET_STATISTICS_PATH
from src.data_loader.candidate_loader import CandidateLoader
from src.utils.artifact_utils import atomic_pickle_dump, get_logger


class DatasetStatistics:
    """Build max-value statistics used by recruiter scoring."""

    def __init__(
        self,
        dataset_path: str = str(DATASET_PATH),
        output_path: str = str(DATASET_STATISTICS_PATH),
    ):
        self.loader = CandidateLoader(dataset_path)
        self.output_path = output_path
        self.logger = get_logger(__name__)

    def build(self) -> dict[str, int | float]:
        """Build and persist dataset statistics."""
        stats = {
            "github_activity_score": 0,
            "profile_completeness_score": 0,
            "recruiter_response_rate": 0,
            "search_appearance_30d": 0,
            "saved_by_recruiters_30d": 0,
            "interview_completion_rate": 0,
            "offer_acceptance_rate": 0,
            "connection_count": 0,
            "endorsements_received": 0,
        }

        total = 0
        for candidate in self.loader.stream_candidates():
            signals = candidate.get("redrob_signals", {})
            for key in stats:
                value = signals.get(key, 0)
                if value > stats[key]:
                    stats[key] = value

            total += 1
            if total % 5000 == 0:
                self.logger.info("Dataset statistics processed %s candidates", total)

        atomic_pickle_dump(stats, self.output_path)

        self.logger.info("Dataset statistics completed for %s candidates", total)
        for key, value in stats.items():
            self.logger.info("%s = %s", key, value)

        return stats
