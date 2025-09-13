import os, sys, pandas as pd, pickle
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from config import settings


# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# Load dataset
df = pd.read_csv(settings.DATA_DIR + "/behavior.csv")

# Train Isolation Forest
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(df)

# Predict anomalies (-1 = anomaly, 1 = normal)
y_pred = model.predict(df)
df["prediction"] = y_pred

# Basic evaluation (simulate ground truth: last 200 rows = anomalies)
true_labels = [1] * (len(df) - 200) + [-1] * 200
print(" Classification Report:\n")
print(classification_report(true_labels, y_pred, target_names=["Normal", "Anomaly"]))

# Save model
with open(settings.MODELS_DIR + "/behavior_model.pkl", "wb") as f:
    pickle.dump(model, f)

print(" Behavior model saved to models/behavior_model.pkl")
