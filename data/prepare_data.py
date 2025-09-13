from datasets import load_dataset
import pandas as pd

print("Downloading dataset...")
ds = load_dataset("zefang-liu/phishing-email-dataset")
df = ds['train'].to_pandas()

# Standardize columns
df = df.rename(columns={"Email Text": "text", "Email Type": "label"})
df['label'] = df['label'].map({"Phishing Email": 1, "Safe Email": 0})

# Drop empty texts
df = df.dropna(subset=["text"]).copy()

# Remove extreme outliers
df["text_length"] = df["text"].str.len()
df = df[(df["text_length"] > 10) & (df["text_length"] < 10000)]

# Remove duplicates
df = df.drop_duplicates(subset="text").copy()

# Save cleaned dataset
df[["text","label"]].to_csv("data/clean_emails.csv", index=False)

print("Saved clean dataset to data/clean_emails.csv with", len(df), "rows")
