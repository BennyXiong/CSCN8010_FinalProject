from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

load_dotenv()  # load from .env
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) 

def generate_answer_with_openai(context: str, question: str, model: str = "gpt-4") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful student success adivor. Use the provided context to answer the student's question. If the answer is not in the context, say 'Sorry, I'm not sure about that.'"
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


def generate_answer_with_ollama(context, query, model="llama3"):
    prompt = f"""You are a helpful student success adivor. Use the provided context to answer the student's question. If the answer is not in the context, say 'Sorry, I'm not sure about that.'

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
