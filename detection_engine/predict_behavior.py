import os, sys, pickle
import pandas as pd

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from config import settings

# Load model
with open(settings.MODELS_DIR + "/behavior_model.pkl", "rb") as f:
    model = pickle.load(f)

def classify_behavior(click_speed, hover_time, link_clicks, login_attempts):
    df = pd.DataFrame([{
        "click_speed": click_speed,
        "hover_time": hover_time,
        "link_clicks": link_clicks,
        "login_attempts": login_attempts
    }])
    pred = model.predict(df)[0]
    return "Anomaly (suspicious behavior)" if pred == -1 else "Normal behavior"

if __name__ == "__main__":
    # Test samples
    sample1 = classify_behavior(0.5, 1.0, 2, 1)   # Normal user
    sample2 = classify_behavior(0.1, 0.1, 10, 5)  # Suspicious user
    
    print("Sample 1:", sample1)
    print("Sample 2:", sample2)
