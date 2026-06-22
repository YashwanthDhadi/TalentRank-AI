"""Generate the final submission CSV from ranked candidates."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter
from src.validation.submission_validator import SubmissionValidator
import pandas as pd

from src.config import DEFAULT_FINAL_TOP_K, JOB_DESCRIPTION_PATH, SUBMISSION_OUTPUT_PATH
from src.data_loader.job_description_loader import JobDescriptionLoader
from src.pipeline.ranking_pipeline import RankingPipeline
from src.reasoning.reason_generator import ReasonGenerator
from src.utils.artifact_utils import ensure_directory, get_logger
from src.jd_understanding.jd_analyzer import JDAnalyzer


class SubmissionGenerator:
    """Generate the submission output without changing ranking behavior."""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.pipeline = RankingPipeline()
        self.loader = JobDescriptionLoader(str(JOB_DESCRIPTION_PATH))

    def generate(
        self,
        output_path: str = str(SUBMISSION_OUTPUT_PATH),
        top_k: int = DEFAULT_FINAL_TOP_K,
    ) -> pd.DataFrame:
        """Generate and save the submission CSV."""
        total_start = perf_counter()
        jd_text = self.loader.load()
        results = self.pipeline.rank(
            jd_text,
            top_k=top_k
        )
        jd = JDAnalyzer(jd_text).analyze()

        if len(results) != top_k:
            raise ValueError(
                f"Expected {top_k} candidates after reranking, but got {len(results)}."
            )

        submission_start = perf_counter()
        submission = []
        candidate_ids = set()

        for rank, candidate in enumerate(results, start=1):
            reasoning = ReasonGenerator.generate(
                candidate["candidate"],
                jd,
                {
                    "semantic_score": candidate["semantic_score"],
                    "recruiter_score": candidate["recruiter_score"],
                    "career_score": candidate["career_score"],
                    "experience_score": candidate["experience_score"],
                },
            )

            if not reasoning or not isinstance(reasoning, str):
                raise ValueError(
                    f"Reasoning generation failed for candidate '{candidate['candidate_id']}'."
                )

            candidate_id = candidate["candidate_id"]
            if candidate_id in candidate_ids:
                raise ValueError(f"Duplicate candidate_id '{candidate_id}' found in results.")
            candidate_ids.add(candidate_id)

            submission.append(
                {
                    "candidate_id": candidate_id,
                    "rank": rank,
                    "score": round(candidate["final_score"], 4),
                    "reasoning": reasoning,
                }
            )

        df = pd.DataFrame(submission, columns=["candidate_id", "rank", "score", "reasoning"])

        SubmissionValidator.validate(submission)

        output = Path(output_path)
        ensure_directory(output.parent)
        df.to_csv(output, index=False)

        submission_generation_time = perf_counter() - submission_start
        total_execution_time = perf_counter() - total_start

        self.logger.info("Submission generation time: %.3fs", submission_generation_time)
        self.logger.info("Top candidate score: %.4f", df.iloc[0]["score"])
        self.logger.info("Bottom candidate score: %.4f", df.iloc[-1]["score"])
        self.logger.info("Total execution time: %.3fs", total_execution_time)
        self.logger.info("Submission generated successfully at '%s'", output)

        return df
