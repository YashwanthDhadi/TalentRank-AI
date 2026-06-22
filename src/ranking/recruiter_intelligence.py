"""Use normalized dataset statistics for recruiter scoring."""

from __future__ import annotations

from src.config import DATASET_STATISTICS_PATH
from src.utils.artifact_utils import load_pickle


class RecruiterIntelligence:
    """Score recruiter-facing candidate signals using cached dataset statistics."""

    REQUIRED_STAT_KEYS = (
        "github_activity_score",
        "profile_completeness_score",
        "recruiter_response_rate",
        "search_appearance_30d",
        "saved_by_recruiters_30d",
        "interview_completion_rate",
        "offer_acceptance_rate",
        "connection_count",
        "endorsements_received",
    )

    def __init__(self):
        self.stats = load_pickle(DATASET_STATISTICS_PATH, "dataset statistics cache")
        if not isinstance(self.stats, dict):
            raise ValueError("Dataset statistics cache must contain a dictionary.")

        missing_keys = [key for key in self.REQUIRED_STAT_KEYS if key not in self.stats]
        if missing_keys:
            raise ValueError(
                "Dataset statistics cache is missing required keys: "
                f"{', '.join(missing_keys)}."
            )

    def score(self, candidate: dict) -> float:
        """Score recruiter-intelligence signals without changing ranking weights."""
        signals = candidate.get("behavioral", {})
        score = 0.0

        score += (
            signals.get("github_activity_score", 0)
            / self._safe_stat("github_activity_score")
        ) * 0.15
        score += (
            signals.get("profile_completeness_score", 0)
            / self._safe_stat("profile_completeness_score")
        ) * 0.15
        score += (
            signals.get("recruiter_response_rate", 0)
            / self._safe_stat("recruiter_response_rate")
        ) * 0.15
        score += (
            signals.get("search_appearance_30d", 0)
            / self._safe_stat("search_appearance_30d")
        ) * 0.10
        score += (
            signals.get("saved_by_recruiters_30d", 0)
            / self._safe_stat("saved_by_recruiters_30d")
        ) * 0.10
        score += (
            signals.get("interview_completion_rate", 0)
            / self._safe_stat("interview_completion_rate")
        ) * 0.10
        score += (
            signals.get("offer_acceptance_rate", 0)
            / self._safe_stat("offer_acceptance_rate")
        ) * 0.10
        score += (
            signals.get("connection_count", 0)
            / self._safe_stat("connection_count")
        ) * 0.05
        score += (
            signals.get("endorsements_received", 0)
            / self._safe_stat("endorsements_received")
        ) * 0.05

        if signals.get("open_to_work_flag"):
            score += 0.03
        if signals.get("verified_email"):
            score += 0.01
        if signals.get("verified_phone"):
            score += 0.01

        notice = signals.get("notice_period_days", 90)
        if notice <= 30:
            score += 0.05
        elif notice <= 60:
            score += 0.03

        return round(min(score, 1.0), 4)

    def _safe_stat(self, key: str) -> float:
        """Return a validated normalization denominator."""
        value = self.stats[key]
        if value <= 0:
            raise ValueError(
                f"Dataset statistics cache has a non-positive value for '{key}'."
            )
        return float(value)
