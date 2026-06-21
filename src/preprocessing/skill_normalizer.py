"""
skill_normalizer.py

Description:
    Normalizes skill names into a consistent format.
"""

from src.preprocessing.text_cleaner import TextCleaner


class SkillNormalizer:

    # synonym dictionary
    SKILL_MAP = {

        "ml": "machine learning",
        "machine-learning": "machine learning",
        "machine_learning": "machine learning",

        "ai": "artificial intelligence",
        "artificial-intelligence": "artificial intelligence",

        "llms": "llm",
        "large language models": "llm",

        "nlp": "natural language processing",

        "cv": "computer vision",

        "js": "javascript",

        "py": "python"
    }

    @classmethod
    def normalize(cls, skill: str) -> str:

        skill = TextCleaner.clean(skill)

        return cls.SKILL_MAP.get(skill, skill)

    @classmethod
    def normalize_list(cls, skills: list[str]) -> list[str]:

        normalized = []

        for skill in skills:

            normalized.append(
                cls.normalize(skill)
            )

        return sorted(set(normalized))