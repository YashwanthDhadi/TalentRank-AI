"""
candidate_features.py

Description:
Extracts numerical features from a parsed candidate.
"""


class CandidateFeatures:

    @staticmethod
    def extract(candidate: dict) -> dict:

        skills = candidate.get("skills", [])

        endorsements = [
            skill.get("endorsements", 0)
            for skill in skills
        ]

        durations = [
            skill.get("duration_months", 0)
            for skill in skills
        ]

        if endorsements:
            avg_endorsements = sum(endorsements) / len(endorsements)
        else:
            avg_endorsements = 0

        if durations:
            avg_duration = sum(durations) / len(durations)
        else:
            avg_duration = 0

        features = {

            "experience":
                candidate.get("experience", 0),

            "skill_count":
                len(skills),

            "career_count":
                len(candidate.get("career_history", [])),

            "education_count":
                len(candidate.get("education", [])),

            "certification_count":
                len(candidate.get("certifications", [])),

            "language_count":
                len(candidate.get("languages", [])),

            "average_endorsements":
                round(avg_endorsements, 2),

            "average_skill_duration":
                round(avg_duration, 2)
        }

        return features