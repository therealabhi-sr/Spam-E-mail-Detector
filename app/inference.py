import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

model_path = BASE_DIR / "models" / "model.pkl"
vectorizer_path = BASE_DIR / "models" / "vectorizer.pkl"

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)


def predict_email(text: str):

    vector = vectorizer.transform([text])

    prediction = model.predict(vector)[0]

    probability = model.predict_proba(vector)[0][1]

    result = "spam" if prediction == 1 else "ham"

    return {
        "prediction": result,
        "confidence": round(float(probability), 4)
    }