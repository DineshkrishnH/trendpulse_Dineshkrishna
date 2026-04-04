import requests
import time
import os
import json
from datetime import datetime

API_TOPSTORIES = "https://hacker-news.firebaseio.com/v0/topstories.json"
API_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"
headers = {"User-Agent": "TrendPulse/1.0"}

# Updated categories with keywords
categories = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"],
    "other": []
}

def assign_category(title):
    for cat, keywords in categories.items():
        if any(keyword.lower() in title.lower() for keyword in keywords):
            return cat
    return "other"

# Step 1 — Fetch top story IDs
try:
    response = requests.get(API_TOPSTORIES, headers=headers)
    response.raise_for_status()
    story_ids = response.json()[:500]
except Exception as e:
    print(f"Failed to fetch top stories: {e}")
    story_ids = []

# Step 2 — Fetch story details and classify
stories = []
category_counts = {cat: 0 for cat in categories}
for story_id in story_ids:
    try:
        response = requests.get(API_ITEM.format(story_id), headers=headers)
        response.raise_for_status()
        story = response.json()
        if not story or "title" not in story:
            continue

        cat = assign_category(story["title"])
        if category_counts[cat] >= 25:
            continue  # skip if category quota reached

        record = {
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": cat,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().isoformat()
        }
        stories.append(record)
        category_counts[cat] += 1

    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")

    # Sleep once per category loop (every 25 stories collected)
    if sum(category_counts.values()) % 25 == 0:
        time.sleep(2)

# Step 3 — Save to JSON
os.makedirs("data", exist_ok=True)
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(stories, f, indent=2)

print(f"Collected {len(stories)} stories in total")
print(f"Saved to {filename}")
