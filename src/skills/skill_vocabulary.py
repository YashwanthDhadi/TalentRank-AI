"""Build a vocabulary of skills present in the dataset."""

from __future__ import annotations

from src.config import DATASET_PATH, SKILL_VOCABULARY_PATH
from src.data_loader.candidate_loader import CandidateLoader
from src.utils.artifact_utils import atomic_pickle_dump, get_logger


class SkillVocabulary:
    """Build and persist the skill vocabulary artifact."""

    def __init__(
        self,
        dataset_path: str = str(DATASET_PATH),
        output_path: str = str(SKILL_VOCABULARY_PATH),
    ):
        self.loader = CandidateLoader(dataset_path)
        self.output_path = output_path
        self.logger = get_logger(__name__)

    def build(self) -> list[str]:
        """Build and save the skill vocabulary."""
        vocabulary: set[str] = set()
        count = 0

        for candidate in self.loader.stream_candidates():
            for skill in candidate.get("skills", []):
                name = skill.get("name", "").strip().lower()
                if name:
                    vocabulary.add(name)

            count += 1
            if count % 5000 == 0:
                self.logger.info("Skill vocabulary processed %s candidates", count)

        result = sorted(vocabulary)
        atomic_pickle_dump(result, self.output_path)

        self.logger.info("Skill vocabulary built with %s unique skills", len(result))
        return result
