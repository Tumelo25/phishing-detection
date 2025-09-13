import os

# Base project directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Paths
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Files
CLEAN_DATA = os.path.join(DATA_DIR, "clean_emails.csv")
MODEL_FILE = os.path.join(MODELS_DIR, "phishing_model.pkl")
VEC_FILE = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")
METRICS_FILE = os.path.join(LOGS_DIR, "metrics.txt")
