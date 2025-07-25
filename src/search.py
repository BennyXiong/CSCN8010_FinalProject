from generateAnswer import generate_answer_with_ollama
from search_engine import VectorSearch

vector_search = VectorSearch()
vector_search.load_index()

def get_answer(query):
    results = vector_search.search(query, top_k=3)

    # Combine top-k chunks into a single context string
    context = "\n\n".join([f"{chunk['content']}" for chunk, _ in results])

    # Generate answer using local LLaMA 3
    return generate_answer_with_ollama(context, query)


answer = get_answer("Hi, I’m trying to figure out how to pay my tuition fees.")
print("Answer:\n", answer)
answer = get_answer("Thanks. Do I need to pay the full amount at once?")
print("Answer:\n", answer)
answer = get_answer("What happens if I miss a payment?")
print("Answer:\n", answer)