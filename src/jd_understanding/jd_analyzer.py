"""
jd_analyzer.py

Description:
Analyzes the Job Description and extracts information
required by the ranking engine.
"""

import re


class JDAnalyzer:

    def __init__(self, jd_text: str):

        self.jd_text = jd_text.lower()

    def analyze(self):

        return {

            "experience": self.extract_experience(),

            "required_skills": self.extract_required_skills(),

            "preferred_skills": self.extract_preferred_skills(),

            "negative_signals": self.extract_negative_signals(),

            "work_mode": self.extract_work_mode()
        }

    def extract_experience(self):

        match = re.search(
            r"experience required:\s*(\d+)\s*[–-]\s*(\d+)",
            self.jd_text
        )

        if match:

            return {
                "min": int(match.group(1)),
                "max": int(match.group(2))
            }

        return {
            "min": 0,
            "max": 100
        }

    def extract_required_skills(self):

        skills = [

            "python",

            "embeddings",

            "retrieval",

            "ranking",

            "llm",

            "sentence-transformers",

            "faiss",

            "pinecone",

            "weaviate",

            "qdrant",

            "milvus",

            "evaluation",

            "ndcg",

            "map",

            "mrr",

            "hybrid search"
        ]

        found = []

        for skill in skills:

            if skill in self.jd_text:

                found.append(skill)

        return sorted(found)

    def extract_preferred_skills(self):

        preferred = [

            "lora",

            "qlora",

            "peft",

            "learning-to-rank",

            "xgboost",

            "marketplace",

            "distributed systems",

            "open source"
        ]

        found = []

        for skill in preferred:

            if skill in self.jd_text:

                found.append(skill)

        return sorted(found)

    def extract_negative_signals(self):

        negatives = [

            "langchain",

            "consulting firms",

            "computer vision",

            "robotics",

            "speech"
        ]

        found = []

        for signal in negatives:

            if signal in self.jd_text:

                found.append(signal)

        return found

    def extract_work_mode(self):

        if "hybrid" in self.jd_text:
            return "hybrid"

        if "remote" in self.jd_text:
            return "remote"

        return "onsite"