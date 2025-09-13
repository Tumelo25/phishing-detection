import pickle, os, sys
from preprocess import clean_text

# Add project root to path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from config import settings

# Load model + vectorizer
with open(settings.MODEL_FILE, "rb") as f:
    model = pickle.load(f)
with open(settings.VEC_FILE, "rb") as f:
    vec = pickle.load(f)

def classify_email(text: str) -> str:
    X = vec.transform([clean_text(text)])
    pred = model.predict(X)[0]
    return "Phishing" if pred == 1 else "Legitimate"

if __name__ == "__main__":
    sample1 = "Dear user, your account has been locked. Click here to verify."
    sample2 = "Hi team, here is the agenda for tomorrow's meeting."
    
    print("Sample 1:", classify_email(sample1))
    print("Sample 2:", classify_email(sample2))
