"""Central configuration for TalentRank-AI backend artifacts and defaults."""

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data" / "raw"
ARTIFACTS_DIR = ROOT_DIR / "artifacts"

DATASET_PATH = DATA_DIR / "candidates.jsonl"
JOB_DESCRIPTION_PATH = DATA_DIR / "job_description.docx"

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
EMBEDDING_BATCH_SIZE = 128

EMBEDDINGS_PATH = ARTIFACTS_DIR / "candidate_embeddings.npy"
CANDIDATE_IDS_PATH = ARTIFACTS_DIR / "candidate_ids.pkl"
CANDIDATE_LOOKUP_PATH = ARTIFACTS_DIR / "candidate_lookup.pkl"
FAISS_INDEX_PATH = ARTIFACTS_DIR / "faiss.index"
DATASET_STATISTICS_PATH = ARTIFACTS_DIR / "dataset_statistics.pkl"
SKILL_VOCABULARY_PATH = ARTIFACTS_DIR / "skill_vocabulary.pkl"
SUBMISSION_OUTPUT_PATH = ARTIFACTS_DIR / "submission.csv"

DEFAULT_RETRIEVAL_TOP_K = 1000
DEFAULT_FINAL_TOP_K = 100
DEFAULT_CANDIDATE_RETRIEVER_TOP_K = 1000

LOG_PROGRESS_EVERY_BATCHES = 10
