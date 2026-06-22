"""
explainability_engine.py

Generates recruiter-friendly explanations
for why a candidate was ranked.
"""


class ExplainabilityEngine:

    @staticmethod
    def explain(candidate):

        reasons = []

        if candidate["semantic_score"] >= 0.75:
            reasons.append(
                f"Strong semantic similarity ({candidate['semantic_score']:.2f})"
            )

        if candidate["experience_score"] >= 0.90:
            reasons.append(
                "Experience closely matches the job requirements."
            )

        elif candidate["experience_score"] >= 0.70:
            reasons.append(
                "Experience is reasonably aligned with the role."
            )

        if candidate["skill_score"] >= 0.60:
            reasons.append(
                "Excellent technical skill match."
            )

        elif candidate["skill_score"] >= 0.30:
            reasons.append(
                "Partial technical skill match."
            )

        if candidate["career_score"] >= 0.80:
            reasons.append(
                "Strong and consistent career progression."
            )

        if candidate["recruiter_score"] >= 0.80:
            reasons.append(
                "Strong recruiter and platform engagement signals."
            )

        if candidate["behavior_score"] >= 0.80:
            reasons.append(
                "High profile completeness and responsiveness."
            )

        return reasons