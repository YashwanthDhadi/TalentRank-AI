"""
skill_ranker.py
"""

from src.ranking.semantic_skill_mapper import SemanticSkillMapper


class SkillRanker:

    @staticmethod
    def score(candidate_skills, jd_skills):

        candidate = [
            skill["name"]
            for skill in candidate_skills
        ]

        candidate = SemanticSkillMapper.expand(candidate)

        jd = SemanticSkillMapper.expand(jd_skills)

        if len(jd) == 0:
            return 0

        matches = candidate.intersection(jd)

        return round(len(matches) / len(jd), 4)