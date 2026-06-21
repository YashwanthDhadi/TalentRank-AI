"""
ranking_pipeline.py

Retrieves candidates using FAISS and
re-ranks them using hybrid scoring.
"""

from src.vector_store.faiss_manager import FAISSManager
from src.data_loader.candidate_loader import CandidateLoader
from src.preprocessing.candidate_parser import CandidateParser

from src.ranking.skill_ranker import SkillRanker
from src.ranking.behavior_ranker import BehaviorRanker
from src.ranking.career_ranker import CareerRanker
from src.ranking.experience_ranker import ExperienceRanker
from src.ranking.hybrid_ranker import HybridRanker

from src.jd_understanding.jd_analyzer import JDAnalyzer


class RankingPipeline:

    def __init__(self):

        self.retriever = FAISSManager()

        self.loader = CandidateLoader(
            "data/raw/candidates.jsonl"
        )

    def rank(self, jd_text, top_k=100):

        analyzer = JDAnalyzer(jd_text)

        jd = analyzer.analyze()

        semantic_results = self.retriever.search(
            jd_text,
            top_k=top_k
        )

        candidate_map = {}

        for candidate in self.loader.stream_candidates():

            candidate_map[
                candidate["candidate_id"]
            ] = candidate

        ranked = []

        for item in semantic_results:

            raw = candidate_map[
                item["candidate_id"]
            ]

            candidate = CandidateParser.parse(raw)

            semantic = item["semantic_score"]

            experience = ExperienceRanker.score(
                candidate["experience"],
                jd["experience"]["min"],
                jd["experience"]["max"]
            )

            skills = SkillRanker.score(
                candidate["skills"],
                jd["required_skills"]
            )

            behavior = BehaviorRanker.score(
                candidate["behavioral"]
            )

            career = CareerRanker.score(
                candidate["career_history"]
            )

            final_score = HybridRanker.rank(
                semantic,
                experience,
                skills,
                behavior,
                career
            )

            ranked.append({

                "candidate_id": candidate["candidate_id"],

                "semantic_score": round(semantic,4),

                "experience_score": round(experience,4),

                "skill_score": round(skills,4),

                "behavior_score": round(behavior,4),

                "career_score": round(career,4),

                "final_score": round(final_score,4)

            })

        ranked.sort(
            key=lambda x: x["final_score"],
            reverse=True
        )

        return ranked