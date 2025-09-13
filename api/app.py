import os, sys, pickle
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add project root to path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from detection_engine.preprocess import clean_text
from config import settings

# Load model + vectorizer
with open(settings.MODEL_FILE, "rb") as f:
    model = pickle.load(f)
with open(settings.VEC_FILE, "rb") as f:
    vec = pickle.load(f)

app = Flask(__name__)
CORS(app)

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.post("/predict")
def predict():
    data = request.get_json(force=True)
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Missing 'text'"}), 400

    X = vec.transform([clean_text(text)])
    y = model.predict(X)[0]
    label = "Phishing" if y == 1 else "Legitimate"

    return jsonify({"label": label})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
