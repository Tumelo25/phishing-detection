import os, sys, pandas as pd, numpy as np

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from config import settings

np.random.seed(42)

# Generate synthetic user behavior data
rows = 5000

data = {
    "click_speed": np.random.normal(0.5, 0.2, rows),   # seconds per click
    "hover_time": np.random.normal(1.2, 0.5, rows),    # seconds on links
    "link_clicks": np.random.poisson(2, rows),         # number of links clicked
    "login_attempts": np.random.poisson(1, rows),      # login retries
}

df = pd.DataFrame(data)

# Inject anomalies (simulate phishing victims)
anomalies = pd.DataFrame({
    "click_speed": np.random.normal(0.1, 0.05, 200),
    "hover_time": np.random.normal(0.1, 0.05, 200),
    "link_clicks": np.random.poisson(8, 200),
    "login_attempts": np.random.poisson(5, 200),
})

df = pd.concat([df, anomalies], ignore_index=True)

# Save
behavior_file = settings.DATA_DIR + "/behavior.csv"
df.to_csv(behavior_file, index=False)
print(f" Saved behavior dataset to {behavior_file} with {len(df)} rows")
