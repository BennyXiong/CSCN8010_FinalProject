# search_engine.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd
import os
import pickle
from glob import glob

class VectorSearch:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.texts = []
    
    def build_index_from_folder(self, folder_path):
        csv_files = glob(os.path.join(folder_path, "*.csv"))
        all_texts = []
        all_records = []

        for path in csv_files:
            df = pd.read_csv(path)
            if {'url', 'chunk_number', 'content'}.issubset(df.columns):
                df = df.fillna('')  # Ensure no NaNs
                all_texts.extend(df['content'].astype(str).tolist())
                all_records.extend(df[['url', 'chunk_number', 'content']].to_dict(orient='records'))

        self.texts = all_records  # Store metadata for each chunk
        embeddings = self.model.encode(all_texts, show_progress_bar=True)
        embeddings = np.array(embeddings).astype('float32')  # FAISS needs float32
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def save_index(self, index_path='data/index/faiss.index', meta_path='data/index/texts.pkl'):
        faiss.write_index(self.index, index_path)
        with open(meta_path, 'wb') as f:
            pickle.dump(self.texts, f)

    def load_index(self, index_path='data/index/faiss.index', meta_path='data/index/texts.pkl'):
        self.index = faiss.read_index(index_path)
        with open(meta_path, 'rb') as f:
            self.texts = pickle.load(f)

    def search(self, query, top_k=5):
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')  # Ensure float32
        D, I = self.index.search(query_embedding, top_k)
        return [(self.texts[i], D[0][rank]) for rank, i in enumerate(I[0])]

searcher = VectorSearch()
searcher.build_index_from_folder('data/raw')
searcher.save_index()
print("✅ Index and metadata saved.")