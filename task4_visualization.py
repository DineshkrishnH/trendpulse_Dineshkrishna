import matplotlib.pyplot as plt
import os
import pandas as pd

#Task 1

df = pd.read_csv("data/trends_analysed.csv")


category_counts = df["category"].value_counts()
categories = category_counts.index
counts = category_counts.values

os.makedirs("outputs", exist_ok=True)

plt.figure(figsize=(8, 5))
plt.bar(categories, counts, color="steelblue")
plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")


plt.savefig("outputs/stories_per_category_bar.png")
plt.show()

#Task 2

top_stories = df.sort_values(by="score", ascending=False).head(10)

plt.figure(figsize=(8, 5))
plt.barh(top_stories["title"], top_stories["score"], color="steelblue")
plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.gca().invert_yaxis()  

plt.savefig("outputs/chart1_top_stories.png")
plt.show()

#Task 3

plt.figure(figsize=(8, 5))
plt.bar(category_counts.index, category_counts.values, color=plt.cm.tab10.colors)

plt.title("Number of Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.savefig("outputs/chart2_categories.png")
plt.show()

# Task 4

popular = df[df["is_popular"] == True]
non_popular = df[df["is_popular"] == False]

plt.figure(figsize=(8, 5))
plt.scatter(popular["score"], popular["num_comments"], 
            color="steelblue", label="Popular Stories", alpha=0.7)
plt.scatter(non_popular["score"], non_popular["num_comments"], 
            color="red", label="Non-Popular Stories", alpha=0.7)

plt.title("Score vs Number of Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.legend()
plt.savefig("outputs/chart3_scatter.png")
plt.show()