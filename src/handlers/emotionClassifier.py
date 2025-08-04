import torch
from transformers import BertTokenizer, BertForSequenceClassification
import torch.nn.functional as F

class EmotionClassifier:
    def __init__(self, model_path, labels):
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
        self.labels = labels

    def predict(self, text, threshold=0.6):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = F.softmax(outputs.logits, dim=1).squeeze().cpu().numpy()

        for label, prob in zip(self.labels, probs):
            if prob >= threshold:
                return label
        return None

# from src.config.config import Config
# config = Config()
# emotionClassifier = EmotionClassifier("models/emotionClassifier", config.emotion_labels)
# print(emotionClassifier.predict("i feel overwhelmed and not sure if i can keep up this term"))