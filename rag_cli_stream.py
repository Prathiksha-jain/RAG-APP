# rag_cli_stream.py
import json
import asyncio
import httpx
from retriever import search

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
#MODEL = "phi3:mini"
MODEL = "tinyllama"

async def stream_answer(question, results):
    context = "\n\n".join(r["text"] for r in results)
    prompt = f"""You are a helpful assistant. Use the context to answer the question clearly.

Context:
{context}

Question:
{question}

Answer:"""

    payload = {"model": MODEL, "prompt": prompt, "stream": True}

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", OLLAMA_URL, json=payload) as response:
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    token = data.get("response", "")
                    print(token, end="", flush=True)
                except Exception:
                    continue
    print("\n" + "-" * 80 + "\n")

async def main():
    print("\n📘 Local RAG CLI (Smart Mode)")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("❓ Question: ").strip()
        if not question or question.lower() == "exit":
            break

        # 👋 Handle greetings & small talk instantly
        normalized = question.lower()
        if any(
            phrase in normalized
            for phrase in [
                "hi", "hello", "hey", "hii",
                "how are", "good morning", "good evening",
                "what's up", "how is it going", "how r u", "how are you"
            ]
        ):
            print("\n💬 I'm doing great! How about you?\n")
            continue

        # 🧠 Decide whether to use RAG or normal chat
        if "document" in normalized:
            print("\n🔎 RAG Mode Triggered — retrieving relevant context...\n")
            results = search(question, k=5)
            if not results:
                print("\n💬 No relevant documents found, switching to chat mode.\n")
                results = [{"text": "You are a helpful assistant. Reply naturally to user queries."}]
        else:
            print("\n💬 Normal Chat Mode (no RAG)\n")
            results = [{"text": "You are a knowledgeable assistant. Answer based on your own understanding."}]

        print("\n💬 Answer (streaming):\n")
        await stream_answer(question, results)


if __name__ == "__main__":
    asyncio.run(main())
