import pandas as pd
import json
import os

filename = "data/trends_20260405.json"

# Load JSON into a DataFrame
df = pd.read_json(filename)
print(f"Loaded {len(df)} stories from {filename}")

# Duplicates — remove any rows with the same post_id
new_df = df.copy()
new_df = new_df.drop_duplicates(subset="post_id", keep="first")
print(f"After removing duplicates: {len(new_df)}")
# Missing values — drop rows where post_id, title, or score is missing
new_df = new_df.dropna(subset=["post_id",'title','score'])

# Ensure score and num_comments are integers
new_df["score"] = new_df["score"].astype(int)
new_df["num_comments"] = new_df["num_comments"].astype(int)
print(f"After removing nulls: {len(new_df)}")

# Remove low-quality stories (score < 5)
new_df = new_df[new_df["score"] >= 5]
print(f"After removing low scores: {len(new_df)}")
# Strip extra whitespace from titles
new_df["title"] = new_df["title"].str.strip()

# Save cleaned DataFrame to CSV
os.makedirs("data", exist_ok=True)
output_file = "data/trends_clean.csv"
new_df.to_csv(output_file, index=False)

# Confirmation message
print(f"Saved {len(new_df)} rows to {output_file}")

# Quick summary: number of stories per category
summary = new_df["category"].value_counts()
print("\nStories per category:")
print(summary)

