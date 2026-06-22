"""
Detect suspicious candidate profiles and return a lightweight penalty.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any


class HoneypotDetector:
    """Simple rule-based checks for inconsistent or unlikely candidate profiles."""

    @staticmethod
    def score(candidate: dict[str, Any]) -> float:
        penalty = 0.0
        experience = float(candidate.get("experience", 0.0))

        if experience < 0 or experience > 50:
            penalty += 0.35

        career_history = candidate.get("career_history", [])
        if HoneypotDetector._has_overlapping_career_entries(career_history):
            penalty += 0.30

        if HoneypotDetector._has_invalid_career_timeline(career_history):
            penalty += 0.25

        skill_durations = [
            float(skill.get("duration_months", 0))
            for skill in candidate.get("skills", [])
            if isinstance(skill, dict)
        ]

        if any(duration > 240 for duration in skill_durations):
            penalty += 0.15

        total_experience_months = sum(skill_durations)
        if experience > 0 and total_experience_months / 12.0 < experience * 0.5:
            penalty += 0.10

        return round(min(penalty, 1.0), 4)

    @staticmethod
    def _has_overlapping_career_entries(career_history: list[dict[str, Any]]) -> bool:
        entries = []
        for entry in career_history:
            start = HoneypotDetector._parse_date(entry.get("start_date"))
            end = HoneypotDetector._parse_date(entry.get("end_date")) or datetime.utcnow().date()
            if start and end:
                entries.append((start, end))
        entries.sort()
        for (start1, end1), (start2, end2) in zip(entries, entries[1:]):
            if start2 < end1:
                return True
        return False

    @staticmethod
    def _has_invalid_career_timeline(career_history: list[dict[str, Any]]) -> bool:
        for entry in career_history:
            start = HoneypotDetector._parse_date(entry.get("start_date"))
            end = HoneypotDetector._parse_date(entry.get("end_date"))
            if start and end and start > end:
                return True
        return False

    @staticmethod
    def _parse_date(value: Any):
        if not isinstance(value, str):
            return None
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        return None
