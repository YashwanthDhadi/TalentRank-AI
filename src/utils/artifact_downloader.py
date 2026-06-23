"""
Download required runtime artifacts from Hugging Face.

This module ensures all required artifacts are available before
the application starts.
"""

from __future__ import annotations

from pathlib import Path

from huggingface_hub import hf_hub_download

from src.config import ARTIFACTS_DIR


class ArtifactDownloader:
    """Download all required artifacts once."""

    REPO_ID = "YashwanthDhadi/talentrank-ai-artifacts"
    REPO_TYPE = "dataset"

    REQUIRED_FILES = (
        "faiss.index",
        "candidate_ids.pkl",
        "candidate_lookup.pkl",
        "dataset_statistics.pkl",
        "skill_vocabulary.pkl",
    )

    @classmethod
    def download(cls) -> None:
        """Download missing artifacts from Hugging Face."""

        ARTIFACTS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        missing = [
            filename
            for filename in cls.REQUIRED_FILES
            if not (ARTIFACTS_DIR / filename).exists()
        ]

        if not missing:
            print("✓ All artifacts already available.")
            return

        print(f"Downloading {len(missing)} missing artifacts...")

        for filename in missing:

            hf_hub_download(
                repo_id=cls.REPO_ID,
                repo_type=cls.REPO_TYPE,
                filename=filename,
                local_dir=ARTIFACTS_DIR,
                local_dir_use_symlinks=False,
            )

            print(f"✓ {filename}")

        print("✓ Artifact download completed.")

    @classmethod
    def verify(cls) -> None:
        """Verify every required artifact exists."""

        missing = []

        for filename in cls.REQUIRED_FILES:

            if not (ARTIFACTS_DIR / filename).exists():
                missing.append(filename)

        if missing:

            raise FileNotFoundError(
                "Missing required artifacts:\n"
                + "\n".join(missing)
            )