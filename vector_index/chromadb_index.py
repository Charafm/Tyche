# chromadb_index.py
import chromadb
from chromadb.config import Settings

class ChromaIndex:
    def __init__(self, persist_directory="chroma_db"):
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            chroma_db_impl="duckdb+parquet"  # or sqlite, etc.
        ))
        self.collection = self.client.get_or_create_collection(
            name="nodes",
            metadata={"hnsw:space": "cosine"}
        )

    def add(self, ids, embeddings, metadatas=None):
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas or [{} for _ in ids]
        )

    def query(self, query_embeddings, n_results=10, where=None):
        # `where` is an optional metadata filter dict
        results = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
            where=where
        )
        return results["ids"], results["distances"]

# Example usage
# idx = ChromaIndex()
# idx.add(["node1"], [[0.1, 0.2, …]])
# ids, scores = idx.query([[0.1, 0.2, …]])
