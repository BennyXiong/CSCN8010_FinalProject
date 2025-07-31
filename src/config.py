from dataclasses import dataclass

@dataclass
class SearchConfig:
    data_folder: str = 'data'
    index_path: str = 'model/faiss.index'
    meta_path: str = 'model/texts.pkl'
    emotion_model_path: str = 'model/emotion_model'
    emotion_labels: list = (
        "anger", "disgust", "fear", "sadness", "annoyance"
    )
