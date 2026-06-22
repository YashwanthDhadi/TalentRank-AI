"""Helpers for artifact validation, loading, and safe replacement."""

from __future__ import annotations

import logging
import os
import pickle
import tempfile
from pathlib import Path
from typing import Any


def get_logger(name: str) -> logging.Logger:
    """Return a configured module logger."""
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        )
    return logging.getLogger(name)


def ensure_file_exists(path: Path | str, description: str) -> Path:
    """Validate that a required file exists and return it as a Path."""
    resolved_path = Path(path)
    if not resolved_path.is_file():
        raise FileNotFoundError(
            f"Required {description} was not found at '{resolved_path}'."
        )
    return resolved_path


def ensure_directory(path: Path | str) -> Path:
    """Create a directory if it does not already exist."""
    resolved_path = Path(path)
    resolved_path.mkdir(parents=True, exist_ok=True)
    return resolved_path


def load_pickle(path: Path | str, description: str) -> Any:
    """Load a pickle file with a meaningful error when it is corrupted."""
    artifact_path = ensure_file_exists(path, description)
    try:
        with artifact_path.open("rb") as file:
            return pickle.load(file)
    except (pickle.PickleError, EOFError, AttributeError, ValueError) as exc:
        raise ValueError(
            f"The {description} at '{artifact_path}' is corrupted or unreadable."
        ) from exc


def atomic_pickle_dump(data: Any, path: Path | str) -> Path:
    """Safely replace a pickle artifact once writing succeeds."""
    artifact_path = Path(path)
    ensure_directory(artifact_path.parent)
    temp_path = create_temp_path(artifact_path)

    with temp_path.open("wb") as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

    os.replace(temp_path, artifact_path)
    return artifact_path


def create_temp_path(path: Path | str) -> Path:
    """Create a temporary path in the same directory as the target artifact."""
    artifact_path = Path(path)
    ensure_directory(artifact_path.parent)
    with tempfile.NamedTemporaryFile(
        dir=artifact_path.parent,
        prefix=f"{artifact_path.stem}_",
        suffix=f"{artifact_path.suffix}.tmp",
        delete=False,
    ) as temp_file:
        return Path(temp_file.name)


def replace_file(temp_path: Path | str, target_path: Path | str) -> Path:
    """Atomically replace a target file with a completed temporary file."""
    target = Path(target_path)
    ensure_directory(target.parent)
    os.replace(Path(temp_path), target)
    return target


def file_size_bytes(path: Path | str) -> int:
    """Return the size of a file in bytes after validating that it exists."""
    return ensure_file_exists(path, "artifact").stat().st_size
