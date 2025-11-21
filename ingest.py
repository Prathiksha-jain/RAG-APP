# ingest.py
from pathlib import Path
import re, json
from pypdf import PdfReader
from docx import Document as DocxDocument
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data")
OUT_DIR.mkdir(exist_ok=True, parents=True)

# Choose an embedding model (local, free, good quality)
# EMB = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
EMB_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMB = SentenceTransformer(EMB_NAME)
DIM = EMB.get_sentence_embedding_dimension()

def clean_text(t: str) -> str:
    t = re.sub(r"\s+", " ", t or "").strip()
    return t

def chunk_text(text: str, max_words=400, overlap=60):
    words = text.split()
    step = max_words - overlap
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i+max_words])
        if chunk.strip():
            yield chunk

def read_pdf(path: Path):
    reader = PdfReader(str(path))
    for i, page in enumerate(reader.pages, start=1):
        txt = clean_text(page.extract_text())
        if not txt:
            continue
        for ch in chunk_text(txt):
            yield ch, {"source": path.name, "page": i}

def read_docx(path: Path):
    doc = DocxDocument(str(path))
    txt = "\n".join(p.text for p in doc.paragraphs)
    txt = clean_text(txt)
    for ch in chunk_text(txt):
        yield ch, {"source": path.name, "page": None}

def build_index():
    chunks, metas = [], []
    for p in RAW_DIR.iterdir():
        if p.suffix.lower() == ".pdf":
            for ch, meta in read_pdf(p):
                chunks.append(ch); metas.append(meta)
        elif p.suffix.lower() in [".docx", ".doc"]:
            for ch, meta in read_docx(p):
                chunks.append(ch); metas.append(meta)
        # Add more parsers if you need (pptx/html/...)
    if not chunks:
        print("No text found. Put files in data/raw/")
        return

    # Embed
    vectors = EMB.encode(chunks, normalize_embeddings=True, convert_to_numpy=True, batch_size=32)
    # Build FAISS index (cosine via normalized vectors -> inner product)
    index = faiss.IndexFlatIP(DIM)
    index.add(vectors)

    np.save(OUT_DIR / "faiss_vectors.npy", vectors)
    (OUT_DIR / "chunks.json").write_text(json.dumps(chunks, ensure_ascii=False), encoding="utf-8")
    (OUT_DIR / "metas.json").write_text(json.dumps(metas, ensure_ascii=False), encoding="utf-8")

    print(f"Indexed {len(chunks)} chunks from {len(list(RAW_DIR.iterdir()))} files.")

if __name__ == "__main__":
    build_index()
