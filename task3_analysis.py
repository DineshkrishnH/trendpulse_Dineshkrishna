import pandas as pd
import numpy as np
import os

# Load the cleaned dataset
filename = "data/trends_clean.csv"
df = pd.read_csv(filename)


print(df.head())
print(df.shape)

# Calculate averages
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"Average score across all stories: {avg_score:.2f}")
print(f"Average number of comments across all stories: {avg_comments:.2f}")


scores = df["score"].to_numpy()

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

highest_score = np.max(scores)
lowest_score = np.min(scores)

print("Mean score:", mean_score)
print("Median score:", median_score)
print("Standard deviation:", std_score)
print("Highest score:", highest_score)
print("Lowest score:", lowest_score)

# --- Category with most stories ---
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print("Category with most stories:", top_category, "(", top_count, ")")

# --- Story with most comments ---
max_comments_idx = df["num_comments"].idxmax()
story_title = df.loc[max_comments_idx, "title"]
comment_count = df.loc[max_comments_idx, "num_comments"]

print("Story with most comments:", story_title, "-", comment_count, "comments") 

# Engagement = num_comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Average score
avg_score = np.mean(df["score"])

df["is_popular"] = df["score"] > avg_score


# Ensure the data folder exists
os.makedirs("data", exist_ok=True)

# Save to a new CSV file
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

# Confirmation message
print(f"Saved {len(df)} rows to {output_file}")
