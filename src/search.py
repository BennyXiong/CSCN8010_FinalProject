from generateAnswer import generate_answer_with_openai, generate_answer_with_ollama
from search_engine import VectorSearch
import os
import warnings
from urllib3.exceptions import NotOpenSSLWarning

class Faq:
    def __init__(self):
        self.vector_search = VectorSearch()
        self.vector_search.load_index()

    def get_answer(self, query):
        results = self.vector_search.search(query, top_k=10)
        # for item in results:
        #     print(item)
        # Combine top-k chunks into a single context string
        context = "\n\n".join([f"{chunk['content']}" for chunk, _ in results])
        if len(context) > 10000:
            context = context[:10000]
        # Generate answer
        return generate_answer_with_ollama(context, query)

os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
faq = Faq()

def answer(question):
    print (f"{question}\n")
    answer = faq.get_answer(question)
    print("Answer:\n", answer)

# answer("Hi, I’m trying to figure out how to pay my tuition fees.")
# print("\n")
# answer("Thanks. Do I need to pay the full amount at once?")
# print("\n")
# answer("What happens if I miss a payment?")
# print("\n")
# answer("How can apply for scholarship")
# print("\n")
answer("any financial assistance available in Ontario")
print("\n")
# answer("When is the last day to drop a course without penalty?")
# print("\n")
# answer("Are there any upcoming student events?")
# print("\n")
# answer("Where can I get help with my resume?")
# print("\n")
answer("is there a place I can do yoga")
print("\n")