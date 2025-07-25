import requests

def generate_answer_with_ollama(context, query, model="llama3"):
    prompt = f"""You are a helpful assistant. Use the context below to answer the user's question concisely and accurately.

Context:
{context}

Question: {query}

Answer:"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False  # Disable streaming for simplicity
        }
    )
    return response.json()['response'].strip()
