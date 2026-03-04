
import pickle
from pathlib import Path

INTENT_MODEL= Path(__file__).parent /'intent_model.pkl'

with open(INTENT_MODEL, "rb") as f:
    pipeline = pickle.load(f)
    

def predict(text):
    probs = pipeline.predict_proba([text])[0]
    label = pipeline.classes_[probs.argmax()]
    confidence = float(probs.max())
    return label, confidence
