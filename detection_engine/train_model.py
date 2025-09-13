import os, sys, pandas as pd, pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix
from preprocess import clean_text

# Add project root to sys.path so we can import config
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from config import settings


# Load cleaned dataset
df = pd.read_csv(settings.CLEAN_DATA)
df["clean"] = df["text"].apply(clean_text)

# Vectorize
vec = TfidfVectorizer(max_features=5000)
X = vec.fit_transform(df["clean"])
y = df["label"]

# Split
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = LinearSVC().fit(Xtr, ytr)

# Evaluate
yp = model.predict(Xte)
cm = confusion_matrix(yte, yp)
report = classification_report(yte, yp)

print(" Confusion Matrix:\n", cm)
print("\n Report:\n", report)

# Save artifacts
with open(settings.MODEL_FILE, "wb") as f: pickle.dump(model, f)
with open(settings.VEC_FILE, "wb") as f: pickle.dump(vec, f)

# Save metrics to file
with open(settings.METRICS_FILE, "w") as f:
    f.write("Confusion Matrix:\n")
    f.write(str(cm))
    f.write("\n\nClassification Report:\n")
    f.write(report)

print(f" Model, vectorizer, and metrics saved to {settings.MODELS_DIR} and {settings.LOGS_DIR}")
