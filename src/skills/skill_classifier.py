"""
skill_classifier.py

Separates extracted terms into
1. Technical Skills
2. Concepts
"""

TECHNICAL_SKILLS = {

    # Languages
    "python",
    "java",
    "c++",
    "go",
    "rust",

    # AI
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "llm",
    "llms",
    "nlp",
    "computer vision",

    # Embeddings
    "embeddings",
    "sentence-transformers",

    # Vector DB
    "faiss",
    "milvus",
    "pinecone",
    "weaviate",
    "qdrant",

    # Search
    "bm25",
    "rag",
    "opensearch",
    "elasticsearch",

    # Fine-tuning
    "lora",
    "qlora",
    "peft",

    # Frameworks
    "langchain",
    "langgraph",
    "haystack",
    "crewai",

    # Cloud
    "aws",
    "azure",
    "gcp",

    # Backend
    "fastapi",
    "flask",
    "docker",
    "kubernetes",
    "spark",
    "sql"
}


class SkillClassifier:

    @staticmethod
    def classify(skills):

        technical = []
        concepts = []

        for skill in skills:

            if skill.lower() in TECHNICAL_SKILLS:
                technical.append(skill)

            else:
                concepts.append(skill)

        return {

            "technical": sorted(technical),

            "concepts": sorted(concepts)

        }