from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # load from .env
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) 

def answer_with_context(context: str, question: str, model: str = "gpt-4") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful student success adivor. Use the provided context to answer the user's question. If the answer is not in the context, say 'I'm not sure based on the provided information.'"
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()