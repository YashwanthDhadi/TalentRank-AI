"""
hybrid_ranker.py

Description:
Calculates the final hybrid ranking score, including a lightweight honeypot penalty.
"""


class HybridRanker:

    WEIGHTS = {
        "semantic": 0.35,
        "skills": 0.20,
        "experience": 0.15,
        "career": 0.10,
        "behavior": 0.05,
        "recruiter": 0.12,
        "honeypot": 0.03,
    }

    @classmethod
    def rank(
        cls,
        semantic_score: float,
        experience_score: float,
        skill_score: float,
        behavior_score: float,
        career_score: float,
        recruiter_score: float,
        honeypot_penalty: float = 0.0,
    ) -> float:
        """Compute a final score with weighted components and a lightweight penalty."""
        final_score = (
            semantic_score * cls.WEIGHTS["semantic"]
            + experience_score * cls.WEIGHTS["experience"]
            + skill_score * cls.WEIGHTS["skills"]
            + behavior_score * cls.WEIGHTS["behavior"]
            + career_score * cls.WEIGHTS["career"]
            + recruiter_score * cls.WEIGHTS["recruiter"]
            - honeypot_penalty * cls.WEIGHTS["honeypot"]
        )
        return round(max(final_score, 0.0), 4)
