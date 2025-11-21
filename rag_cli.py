# rag_cli.py
import asyncio
from retriever import search
from llm import answer

async def main():
    print("\n📘 Local RAG CLI — ask anything from your documents.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("❓ Question: ").strip()
        if not question or question.lower() == "exit":
            break

        print("\n🔎 Retrieving relevant context...")
        results = search(question, k=5)

        print("🧠 Generating answer (using Ollama locally)...\n")
        reply, _ = await answer(question, results)

        print("💬 Answer:\n")
        print(reply)
        print("\n" + "-" * 80 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
