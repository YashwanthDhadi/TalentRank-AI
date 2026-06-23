"""Retrieve candidates using FAISS and re-rank them with hybrid scoring."""

from __future__ import annotations

from time import perf_counter
from typing import Any

from src.config import (
    CANDIDATE_LOOKUP_PATH,
    DEFAULT_RETRIEVAL_TOP_K,
)
from src.jd_understanding.jd_analyzer import JDAnalyzer
from src.ranking.behavior_ranker import BehaviorRanker
from src.ranking.career_ranker import CareerRanker
from src.ranking.experience_ranker import ExperienceRanker
from src.ranking.hybrid_ranker import HybridRanker
from src.ranking.recruiter_intelligence import RecruiterIntelligence
from src.ranking.skill_ranker import SkillRanker
from src.utils.artifact_utils import (
    get_logger,
    load_pickle,
)
from src.validation.honeypot_detector import HoneypotDetector
from src.vector_store.faiss_manager import FAISSManager


class RankingPipeline:
    """Rank candidates using semantic retrieval followed by hybrid scoring."""

    def __init__(self):

        self.logger = get_logger(__name__)

        self.retriever = FAISSManager()

        self.candidate_lookup = load_pickle(
            CANDIDATE_LOOKUP_PATH,
            "candidate lookup cache",
        )

        if (
            not isinstance(self.candidate_lookup, dict)
            or not self.candidate_lookup
        ):
            raise ValueError(
                f"The candidate lookup cache at "
                f"'{CANDIDATE_LOOKUP_PATH}' is empty or invalid."
            )

        self.total_candidates = len(
            self.candidate_lookup
        )

        self.logger.info(
            "Loaded %s candidate profiles.",
            self.total_candidates,
        )

        self.recruiter = RecruiterIntelligence()

        self.honeypot_detector = HoneypotDetector()

    def rank(
        self,
        jd_text: str,
        top_k: int = DEFAULT_RETRIEVAL_TOP_K,
    ) -> list[dict[str, Any]]:
        """Rank candidates for a job description."""

        if top_k <= 0:
            raise ValueError(
                "top_k must be a positive integer."
            )

        total_start = perf_counter()

        analyzer = JDAnalyzer(jd_text)

        jd = analyzer.analyze()

        retrieval_start = perf_counter()

        retrieval_top_k = max(
            DEFAULT_RETRIEVAL_TOP_K,
            top_k,
        )

        semantic_results = self.retriever.search(
            jd_text,
            top_k=retrieval_top_k,
        )

        retrieval_time = (
            perf_counter() - retrieval_start
        )

        if not semantic_results:
            raise ValueError(
                "FAISS returned no matching candidates."
            )

        reranking_start = perf_counter()

        ranked: list[dict[str, Any]] = []



        for item in semantic_results:

            candidate_id = item["candidate_id"]

            candidate = self.candidate_lookup.get(
                candidate_id
            )

            if candidate is None:

                raise ValueError(
                    "Candidate lookup cache does not contain "
                    f"candidate_id '{candidate_id}' referenced "
                    "by the FAISS index."
                )

            semantic = item["semantic_score"]

            experience = ExperienceRanker.score(
                candidate["experience"],
                jd["experience"]["min"],
                jd["experience"]["max"],
            )

            skills = SkillRanker.score(
                candidate["skills"],
                jd["required_skills"],
            )

            behavior = BehaviorRanker.score(
                candidate["behavioral"],
            )

            career = CareerRanker.score(
                candidate["career_history"],
            )

            recruiter = self.recruiter.score(
                candidate,
            )

            honeypot_penalty = self.honeypot_detector.score(
                candidate,
            )

            final_score = HybridRanker.rank(
                semantic,
                experience,
                skills,
                behavior,
                career,
                recruiter,
                honeypot_penalty=honeypot_penalty,
            )

            ranked.append(
                {
                    "candidate_id": candidate["candidate_id"],

                    # Full candidate profile
                    "candidate": candidate,

                    # Individual Scores
                    "semantic_score": round(semantic, 4),
                    "experience_score": round(experience, 4),
                    "skill_score": round(skills, 4),
                    "behavior_score": round(behavior, 4),
                    "career_score": round(career, 4),
                    "recruiter_score": round(recruiter, 4),
                    "honeypot_penalty": round(
                        honeypot_penalty,
                        4,
                    ),

                    # Final Hybrid Score
                    "final_score": round(
                        final_score,
                        4,
                    ),
                }
            )

        ranked.sort(

            key=lambda item: (

                -item["final_score"],

                -item["semantic_score"],

                item["candidate_id"],

            )

        )

        reranking_time = (
            perf_counter()
            - reranking_start
        )

        total_execution_time = (
            perf_counter()
            - total_start
        )

        final_results = ranked[:top_k]

        self.logger.info("-" * 60)

        self.logger.info(
            "Ranking Summary"
        )

        self.logger.info(
            "Candidates Available : %s",
            self.total_candidates,
        )

        self.logger.info(
            "Retrieved           : %s",
            len(semantic_results),
        )

        self.logger.info(
            "Returned            : %s",
            len(final_results),
        )

        self.logger.info(
            "Retrieval Time      : %.3fs",
            retrieval_time,
        )

        self.logger.info(
            "Reranking Time      : %.3fs",
            reranking_time,
        )

        self.logger.info(
            "Total Time          : %.3fs",
            total_execution_time,
        )

        self.logger.info("-" * 60)

        return final_results