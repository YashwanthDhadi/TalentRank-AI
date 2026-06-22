from src.pipeline.embedding_cache import EmbeddingCache

def main():

    cache = EmbeddingCache()

    cache.build()   # IMPORTANT: no limit=100

if __name__ == "__main__":
    main()