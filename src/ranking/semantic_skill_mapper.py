"""
semantic_skill_mapper.py

Description:
Maps related skills into semantic groups so that
the ranker understands equivalent technologies.
"""


class SemanticSkillMapper:

    SKILL_GROUPS = {

        "vector_database": {
            "faiss",
            "milvus",
            "pinecone",
            "weaviate",
            "qdrant",
            "chromadb"
        },

        "llm": {
            "llm",
            "large language model",
            "large language models",
            "lora",
            "qlora",
            "peft",
            "transformers"
        },

        "retrieval": {
            "retrieval",
            "rag",
            "semantic search",
            "vector search",
            "dense retrieval"
        },

        "embeddings": {
            "embeddings",
            "sentence-transformers",
            "bge",
            "e5",
            "openai embeddings"
        },

        "nlp": {
            "nlp",
            "natural language processing",
            "text mining"
        },

        "machine_learning": {
            "machine learning",
            "deep learning",
            "artificial intelligence",
            "ai"
        }
    }

    @classmethod
    def expand(cls, skills):

        expanded = set()

        for skill in skills:

            skill = skill.lower()

            expanded.add(skill)

            for values in cls.SKILL_GROUPS.values():

                if skill in values:
                    expanded.update(values)

        return expanded