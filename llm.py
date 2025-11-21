import httpx
import json
import asyncio

async def answer_ollama(question, context):
    """
    Calls Ollama locally (tinyllama model) with streaming enabled.
    Optimized for faster CPU performance and live output.
    """
    url = "http://localhost:11434/api/generate"  # Use localhost, not 127.0.0.1
    prompt = f"""You are a helpful assistant. 
Use the following context to answer concisely.

Context:
{context}

Question: {question}
Answer:"""

    payload = {
        "model": "tinyllama",
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_predict": 120,       # limit output length for speed
            "temperature": 0.4,       # make answers consistent
            "top_p": 0.9
        }
    }

    print("💬 Answer (streaming):\n")
    async with httpx.AsyncClient(timeout=None, trust_env=False) as client:
        async with client.stream("POST", url, json=payload) as response:
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    if "response" in data:
                        print(data["response"], end="", flush=True)  # live typing
                    if data.get("done", False):
                        print("\n" + "-" * 80)
                        return
                except json.JSONDecodeError:
                    continue
