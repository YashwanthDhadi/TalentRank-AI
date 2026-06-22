"""
submission_validator.py

Validates the final submission before writing CSV.
"""

from __future__ import annotations


class SubmissionValidator:
    """Validate the final submission."""

    @staticmethod
    def validate(results: list[dict]) -> None:

        # --------------------------------------------
        # Exactly 100 candidates
        # --------------------------------------------

        if len(results) != 100:
            raise ValueError(
                f"Submission must contain exactly 100 candidates. "
                f"Found {len(results)}."
            )

        # --------------------------------------------
        # Candidate IDs
        # --------------------------------------------

        candidate_ids = [
            row["candidate_id"]
            for row in results
        ]

        if len(candidate_ids) != len(set(candidate_ids)):
            raise ValueError(
                "Duplicate candidate_id found."
            )

        # --------------------------------------------
        # Rank Validation
        # --------------------------------------------

        ranks = [
            row["rank"]
            for row in results
        ]

        expected = list(range(1, 101))

        if sorted(ranks) != expected:
            raise ValueError(
                "Ranks must contain every integer "
                "from 1 to 100 exactly once."
            )

        # --------------------------------------------
        # Score Validation
        # --------------------------------------------

        scores = [
            row["score"]
            for row in results
        ]

        for i in range(len(scores) - 1):

            if scores[i] < scores[i + 1]:

                raise ValueError(
                    "Scores must be monotonically "
                    "non-increasing."
                )

        # --------------------------------------------
        # Reasoning Validation
        # --------------------------------------------

        for row in results:

            reasoning = row.get(
                "reasoning",
                ""
            ).strip()

            if reasoning == "":
                raise ValueError(
                    f"Candidate {row['candidate_id']} "
                    "has empty reasoning."
                )

        # --------------------------------------------
        # Candidate ID Format
        # --------------------------------------------

        for row in results:

            candidate_id = row["candidate_id"]

            if not candidate_id.startswith("CAND_"):

                raise ValueError(
                    f"Invalid candidate_id "
                    f"{candidate_id}"
                )

        return