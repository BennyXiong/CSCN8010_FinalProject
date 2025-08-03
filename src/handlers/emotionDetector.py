import torch
from transformers import BertTokenizer, BertForSequenceClassification
import torch.nn.functional as F

class EmotionDetector:
    def __init__(self, model_path, labels):
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
        self.labels = labels

    def detect(self, text, threshold=0.7):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = F.softmax(outputs.logits, dim=1).squeeze().cpu().numpy()

        return [
            (label, float(prob))
            for label, prob in zip(self.labels, probs)
            if prob >= threshold
        ]