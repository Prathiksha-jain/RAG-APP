# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from retriever import search
from llm import answer
import uvicorn
import asyncio

app = FastAPI(title="RAG App")

class Ask(BaseModel):
    question: str
    top_k: int = 12

@app.post("/ask")
async def ask(q: Ask):
    results = search(q.question, q.top_k)
    content, used = await answer(q.question, results)
    sources = []
    for i, r in enumerate(used, start=1):
        s = {"id": i, "source": r["meta"]["source"]}
        if r["meta"].get("page"):
            s["page"] = r["meta"]["page"]
        sources.append(s)
    return {"answer": content, "sources": sources}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
