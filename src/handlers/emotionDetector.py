import torch
from transformers import BertTokenizer, BertForSequenceClassification

class EmotionDetector:
    def __init__(self, model_path, labels):
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
        self.labels = labels

    def detect(self, text, threshold=0.5):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.sigmoid(outputs.logits).squeeze().cpu().numpy()

            # Filter only labels above the threshold
            filtered = [
                (label, float(prob))
                for label, prob in zip(self.labels, probs)
                if prob >= threshold
            ]

            # If none meet the threshold, return None
            if not filtered:
                return None

            # Return the one with the highest probability
            return max(filtered, key=lambda x: x[1])