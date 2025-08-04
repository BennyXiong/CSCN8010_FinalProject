import os
import warnings
from urllib3.exceptions import NotOpenSSLWarning
from src.handlers.answerGenerator import AnswerGenerator
from src.handlers.searchEngine import FaissSearchEngine

class ChatbotController:
    def __init__(self):
        self.vector_search = FaissSearchEngine()
        self.answer_generator = AnswerGenerator()

    def get_answer(self, query):
        results = self.vector_search.search(query, top_k=10)
        # Combine top-k chunks into a single context string
        context = "\n\n".join([f"{chunk['content']}" for chunk, _ in results])
        if len(context) > 10000:
            context = context[:10000]
        # Generate answer
        return self.answer_generator.generate_answer_with_openai(context, query)

# os.environ["TOKENIZERS_PARALLELISM"] = "false"
# warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
# chatbot = ChatbotController()

# def answer(question):
#     print (f"{question}\n")
#     answer = chatbot.get_answer(question)
#     print(f"Answer:\n{answer}\n")

# questions = [
    # "Hi, I'm trying to figure out how to pay my tuition fees.",
    # "Thanks. Do I need to pay the full amount at once?",
    # "How do I make a payment?",
    # "What happens if I miss a payment?",
    # "Can I have an extension/ instalment plan of my payment due",
    # "Why has my payment not been posted to the Student Portal/ Can you confirm my payment",
    # "How do I pay for a course on Held Enrolment",
    # "How can apply for scholarship",
    # "any financial assistance available in Ontario",
    # "When is the last day to drop a course without penalty",
    # "Are there any upcoming student events",
    # "Where can I get help with my resume",
    # "is there a place I can do yoga",
    # "How to View my Timetable",
    # "I can't see my Timetable",
    # "How do I withdraw from my program",
    # "How do I change my block or add/drop a course"
# ]

# for question in questions:
#     answer(question)