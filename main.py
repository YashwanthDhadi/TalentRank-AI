from pprint import pprint

from src.pipeline.ranking_pipeline import RankingPipeline
from src.data_loader.job_description_loader import JobDescriptionLoader

loader = JobDescriptionLoader(
    "data/raw/job_description.docx"
)

jd = loader.load()

pipeline = RankingPipeline()

results = pipeline.rank(
    jd,
    top_k=10
)

pprint(results)