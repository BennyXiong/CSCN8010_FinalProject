import re
import nltk
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Conv1D, GlobalMaxPooling1D
import pandas as pd
from sentence_transformers import SentenceTransformer

EMOTIONS = ['neutral', 'confused', 'frustrated', 'angry', 'anxious', 'happy']


df = pd.read_csv("data/goemotions_1.csv")
emotion_cols = [
    'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring', 'confusion', 'curiosity', 'desire',
    'disappointment', 'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief',
    'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization', 'relief', 'remorse', 'sadness',
    'surprise', 'neutral'
]
df = df[df['example_very_unclear'] == 0]

# Get embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

X = model.encode(df['text'].tolist(), batch_size=64, show_progress_bar=True)
y_onehot = df[emotion_cols].values

# Hybrid LSTM + CNN
model = Sequential([
    Embedding(input_dim=10000, output_dim=128, input_length=50),
    Bidirectional(LSTM(64, return_sequences=True)),
    Conv1D(64, kernel_size=3, activation='relu'),
    GlobalMaxPooling1D(),
    Dense(32, activation='relu'),
    Dense(len(EMOTIONS), activation='softmax')
])

# Compile and Train
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X, y_onehot, epochs=5, batch_size=32, validation_split=0.1)

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # remove punctuation/numbers
    text = re.sub(r"\s+", " ", text).strip() # remove extra spaces
    return text

def predict_emotion(text):
    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    seq = tokenizer.texts_to_sequences([clean_text(text)])
    padded = pad_sequences(seq, maxlen=50, padding="post")
    pred = model.predict(padded)
    emotion = EMOTIONS[np.argmax(pred)]
    return emotion