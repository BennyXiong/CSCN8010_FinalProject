import torch
from transformers import BertTokenizer, BertForSequenceClassification

class IntentClassifier():
    def __init__(self, model_path, labels):
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
        self.labels = labels

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            predicted_class_id = outputs.logits.argmax().item()
        return self.labels[predicted_class_id]

# from src.config.config import Config
# config = Config()
# intentClassifier = IntentClassifier("models/intentClassifier", config.intent_labels)
# print(intentClassifier.predict("Hi, I'm trying to figure out how to pay my tuition fees."))
# print(intentClassifier.predict("When is the tuition payment deadline"))
# print(intentClassifier.predict("Are there any upcoming student events"))