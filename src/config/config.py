from dataclasses import dataclass

@dataclass
class Config:
    data_folder: str = '../data'
    index_path: str = '../model/faiss.index'
    meta_path: str = '../model/texts.pkl'
    emotion_model_path: str = '../model'
    emotion_labels: list = ["sadness", "grief", "fear", "remorse", "disappointment", "nervousness", "embarrassment" ]
