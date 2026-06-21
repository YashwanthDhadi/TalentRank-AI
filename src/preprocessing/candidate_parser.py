"""
candidate_parser.py

Description:
    Parses raw candidate dictionaries into a standardized format.
"""

from src.preprocessing.text_cleaner import TextCleaner
from src.preprocessing.skill_normalizer import SkillNormalizer


class CandidateParser:
    @staticmethod
    def parse(candidate: dict) -> dict:
        profile = candidate.get("profile", {})
        signals = candidate.get("redrob_signals", {})

        parsed = {
            "candidate_id": candidate.get("candidate_id"),

            "headline": TextCleaner.clean(
                profile.get("headline", "")
            ),

            "summary": TextCleaner.clean(
                profile.get("summary", "")
            ),

            "country": profile.get("country", ""),

            "experience": profile.get(
                "years_of_experience", 0
            ),

            "current_title": TextCleaner.clean(
                profile.get("current_title", "")
            ),

            "current_company": profile.get(
                "current_company", ""
            ),

            "skills": [
                {
                    "name": SkillNormalizer.normalize(
                        skill.get("name", "")
                    ),
                    "proficiency": skill.get(
                        "proficiency"
                    ),
                    "endorsements": skill.get(
                        "endorsements", 0
                    ),
                    "duration_months": skill.get(
                        "duration_months", 0
                    ),
                }
                for skill in candidate.get("skills", [])
            ],

            "education": candidate.get(
                "education", []
            ),

            "career_history": candidate.get(
                "career_history", []
            ),

            "certifications": candidate.get(
                "certifications", []
            ),

            "languages": candidate.get(
                "languages", []
            ),

            "behavioral": signals,
        }

        return parsed