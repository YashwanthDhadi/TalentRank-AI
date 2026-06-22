"""Extract job-description skills from the cached vocabulary."""

from __future__ import annotations

from src.config import SKILL_VOCABULARY_PATH
from src.utils.artifact_utils import load_pickle


class JDSkillExtractor:
    """Extract skills from a job description using the cached vocabulary."""

    def __init__(self, vocabulary_path: str = str(SKILL_VOCABULARY_PATH)):
        self.vocabulary = load_pickle(vocabulary_path, "skill vocabulary cache")
        if not isinstance(self.vocabulary, list):
            raise ValueError("Skill vocabulary cache must contain a list.")

    def extract(self, jd_text: str) -> list[str]:
        """Extract matched skills from the job description text."""
        jd_text = jd_text.lower()
        skills = []
        for skill in self.vocabulary:
            if skill in jd_text:
                skills.append(skill)
        return sorted(skills)
