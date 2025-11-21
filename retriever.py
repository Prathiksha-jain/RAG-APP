# retriever.py
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
EMB = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# EMB = SentenceTransformer("intfloat/multilingual-e5-large")
DIM = EMB.get_sentence_embedding_dimension()

VEC = np.load("data/faiss_vectors.npy")
chunks = json.loads(open("data/chunks.json","r",encoding="utf-8").read())
metas  = json.loads(open("data/metas.json","r",encoding="utf-8").read())

index = faiss.IndexFlatIP(DIM)
index.add(VEC)

def search(query: str, k: int = 12):
    q = EMB.encode([query], normalize_embeddings=True, convert_to_numpy=True)
    D, I = index.search(q, k)
    out = []
    for rank, idx in enumerate(I[0], start=1):
        out.append({
            "rank": rank,
            "score": float(D[0][rank-1]),
            "text": chunks[idx],
            "meta": metas[idx],
        })
    return out
