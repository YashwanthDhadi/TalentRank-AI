"""
hybrid_ranker.py

Description:
Calculates the final hybrid ranking score.
"""


class HybridRanker:

    WEIGHTS = {
        "semantic": 0.40,
        "experience": 0.20,
        "skills": 0.20,
        "behavior": 0.10,
        "career": 0.10
    }

    @classmethod
    def rank(
        cls,
        semantic_score: float,
        experience_score: float,
        skill_score: float,
        behavior_score: float,
        career_score: float
    ):

        final_score = (

            semantic_score * cls.WEIGHTS["semantic"]

            + experience_score * cls.WEIGHTS["experience"]

            + skill_score * cls.WEIGHTS["skills"]

            + behavior_score * cls.WEIGHTS["behavior"]

            + career_score * cls.WEIGHTS["career"]

        )

        return round(final_score, 4)