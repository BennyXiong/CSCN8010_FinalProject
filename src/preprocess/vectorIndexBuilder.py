# search_engine.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd
import os
import pickle
from glob import glob
from config.config import Config

class VectorIndexBuilder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
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

        # Convert each dict to a tuple of its items (which is hashable), deduplicate, then convert back to dict
        unique_records = list({tuple(d.items()) for d in all_records})
        self.texts = [dict(t) for t in unique_records]
        embeddings = self.model.encode(all_texts, show_progress_bar=True)
        embeddings = np.array(embeddings).astype('float32')  # FAISS needs float32
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def save_index(self, index_path='model/faiss.index', meta_path='model/texts.pkl'):
        faiss.write_index(self.index, index_path)
        with open(meta_path, 'wb') as f:
            pickle.dump(self.texts, f)

config = Config()
builder = VectorIndexBuilder()
builder.build_index_from_folder(config.data_folder)
builder.save_index(index_path=config.index_path, meta_path=config.meta_path)
print("✅ Index and metadata saved.")