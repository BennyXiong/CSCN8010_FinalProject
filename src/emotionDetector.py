import torch
from transformers import BertTokenizer, BertForSequenceClassification

class EmotionDetector:
    def __init__(self, model_path, labels=None):
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
        self.labels = labels or [
            "anger", "disgust", "fear", "sadness", "annoyance"
        ]

    def detect(self, text, threshold=0.5):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.sigmoid(outputs.logits).squeeze().cpu().numpy()

        return [
            (label, float(prob))
            for label, prob in zip(self.labels, probs)
            if prob >= threshold
        ]
