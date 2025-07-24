from search_engine import VectorSearch

searcher = VectorSearch()
searcher.load_index()

query = "Hi, I’m trying to figure out how to pay my tuition fees"
results = searcher.search(query)

for i, (text, score) in enumerate(results):
    print(f"{i+1}. Score: {score:.2f} - {text[:200]}...\n")