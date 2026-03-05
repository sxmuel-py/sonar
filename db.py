import os
import json
import numpy as np
from pathlib import Path
from config import DB_DIR

DB_FILE = DB_DIR / "vectors.npz"
META_FILE = DB_DIR / "metadata.json"

class NumpyVectorDB:
    """A lightweight, custom vector database using raw numpy.
    This replaces Heavy dependencies like ChromaDB/Pydantic that break on Python 3.14."""
    def __init__(self):
        self.embeddings = []
        self.metadatas = []
        self.documents = []
        self.load()

    def load(self):
        if DB_FILE.exists() and META_FILE.exists():
            with open(META_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.metadatas = data["metadatas"]
                self.documents = data["documents"]
            
            try:
                data = np.load(str(DB_FILE))
                self.embeddings = data["embeddings"].tolist()
            except Exception:
                pass
            
    def save(self):
        DB_DIR.mkdir(parents=True, exist_ok=True)
        with open(META_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "metadatas": self.metadatas,
                "documents": self.documents
            }, f)
            
        if self.embeddings:
            np.savez_compressed(str(DB_FILE), embeddings=np.array(self.embeddings, dtype=np.float32))

    def add(self, embeddings, metadatas, documents, ids=None):
        self.embeddings.extend(embeddings)
        self.metadatas.extend(metadatas)
        self.documents.extend(documents)
        
    def query(self, query_embeddings, n_results=5, include=None):
        if not self.embeddings:
            return {"ids": [[]], "distances": [[]], "metadatas": [[]], "documents": [[]]}
            
        q_emb = np.array(query_embeddings[0], dtype=np.float32)
        db_emb = np.array(self.embeddings, dtype=np.float32)
        
        # Normalize vectors for cosine similarity
        q_norm = np.linalg.norm(q_emb)
        db_norms = np.linalg.norm(db_emb, axis=1)
        
        q_norm = q_norm if q_norm != 0 else 1
        db_norms[db_norms == 0] = 1
        
        # Calculate Cosine similarity
        similarities = np.dot(db_emb, q_emb) / (db_norms * q_norm)
        
        # Convert similarity to 'distance' (0 is identical)
        distances = 1 - similarities
        
        # Get indices of the smallest distances
        top_indices = np.argsort(distances)[:n_results]
        
        return {
            "ids": [["id_" + str(i) for i in top_indices]],
            "distances": [[distances[i] for i in top_indices]],
            "metadatas": [[self.metadatas[i] for i in top_indices]],
            "documents": [[self.documents[i] for i in top_indices]]
        }

    def clear(self):
        self.embeddings = []
        self.metadatas = []
        self.documents = []
        if DB_FILE.exists():
            DB_FILE.unlink()
        if META_FILE.exists():
            META_FILE.unlink()

# Singleton instance
_db_instance = None

def get_collection():
    global _db_instance
    if _db_instance is None:
        _db_instance = NumpyVectorDB()
    return _db_instance
