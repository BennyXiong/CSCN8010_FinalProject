from generateAnswer import generate_answer_with_ollama
from search_engine import VectorSearch

class Faq:
    def __init__(self):
        self.vector_search = VectorSearch()
        self.vector_search.load_index()

    def get_answer(self, query):
        results = self.vector_search.search(query, top_k=3)

        # Combine top-k chunks into a single context string
        context = "\n\n".join([f"{chunk['content']}" for chunk, _ in results])
        # Generate answer using local LLaMA 3
        return generate_answer_with_ollama(context, query)

faq = Faq()

def answer(question):
    print (f"{question}\n")
    answer = faq.get_answer(question)
    print("Answer:\n", answer)

answer("Hi, I’m trying to figure out how to pay my tuition fees.")
print("\n")
answer("Thanks. Do I need to pay the full amount at once?")
print("\n")
answer("What happens if I miss a payment?")
print("\n")
answer("How can apply for scholarship")
print("\n")
answer("any financial assistant available")