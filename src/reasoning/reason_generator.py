"""
reason_generator.py

Generates human-readable reasoning for the final submission.

The reasoning is factual and uses only information present
in the candidate profile and ranking scores.

No hallucinations.
No external APIs.
"""

from __future__ import annotations


class ReasonGenerator:
    """Generate concise candidate-specific reasoning."""

    @staticmethod
    def generate(candidate: dict, jd: dict, scores: dict) -> str:
        """
        Generate a submission reasoning string.

        Parameters
        ----------
        candidate : dict
            Parsed candidate.

        jd : dict
            Parsed job description.

        scores : dict
            Contains semantic, skill, recruiter, career,
            experience and final scores.

        Returns
        -------
        str
        """

        reasons = []

        # --------------------------------------------------
        # Experience
        # --------------------------------------------------

        experience = candidate.get("experience", 0)

        if experience > 0:
            reasons.append(
                f"{experience:.1f} years of experience"
            )

        # --------------------------------------------------
        # Current title
        # --------------------------------------------------

        title = candidate.get("current_title", "").strip()

        if title:
            reasons.append(title)

        # --------------------------------------------------
        # Skill Matching
        # --------------------------------------------------

        candidate_skill_names = {
            skill.get("name", "").lower()
            for skill in candidate.get("skills", [])
        }

        required = set(
            map(
                str.lower,
                jd.get("required_skills", [])
            )
        )

        matched = sorted(candidate_skill_names & required)

        if matched:

            top_skills = matched[:4]

            reasons.append(
                "Matches skills: "
                + ", ".join(top_skills)
            )

        else:

            reasons.append(
                "Limited required skill overlap"
            )

        # --------------------------------------------------
        # Semantic Similarity
        # --------------------------------------------------

        semantic = scores.get("semantic_score", 0)

        if semantic >= 0.80:

            reasons.append(
                "Excellent semantic alignment"
            )

        elif semantic >= 0.70:

            reasons.append(
                "Strong semantic alignment"
            )

        elif semantic >= 0.60:

            reasons.append(
                "Reasonable semantic alignment"
            )

        # --------------------------------------------------
        # Recruiter Signals
        # --------------------------------------------------

        recruiter = scores.get("recruiter_score", 0)

        if recruiter >= 0.90:

            reasons.append(
                "Strong recruiter engagement"
            )

        elif recruiter >= 0.70:

            reasons.append(
                "Good recruiter engagement"
            )

        # --------------------------------------------------
        # Career Progression
        # --------------------------------------------------

        career = scores.get("career_score", 0)

        if career >= 0.80:

            reasons.append(
                "Consistent career progression"
            )

        # --------------------------------------------------
        # Weaknesses
        # --------------------------------------------------

        missing = sorted(required - candidate_skill_names)

        if missing:

            reasons.append(
                "Gap: "
                + ", ".join(missing[:2])
            )

        # --------------------------------------------------
        # Final reasoning
        # --------------------------------------------------

        reasoning = ". ".join(reasons)

        if not reasoning.endswith("."):
            reasoning += "."

        return reasoning