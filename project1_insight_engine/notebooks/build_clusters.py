# =============================================================================
# SCRIPT: build_clusters.py
# GOAL:   Take the saved meaning-vectors (embeddings) and GROUP the complaints
#         into themes ("circle the crowds on the meaning map"). Then describe
#         each theme with its top keywords + real example complaints, and save.
#
# PLAIN VERSION:
#   - Each complaint is already a dot on a "meaning map" (the embeddings).
#   - CLUSTERING = find the crowds of dots. Each crowd = a common problem/theme.
#   - We use KMeans, which splits the dots into K groups. We pick K and can adjust.
#   - Then for each group we find the words that make it special (using TF-IDF)
#     and pull 2 real complaints so we can SEE what the theme is.
#
# OUTPUT: data/sample_clustered.parquet  (complaints + their theme number)
#         prints a readable summary of every theme.
# =============================================================================

import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "data")

# How many themes to split into. Not too few (vague) or too many (fragmented).
# 12 is a sensible starting point for one product; easy to change.
N_THEMES = 12
RANDOM_SEED = 42

# 1) Load the sample complaints and their saved meaning-vectors (aligned by row).
df = pd.read_parquet(os.path.join(DATA, "sample_complaints.parquet"))
emb = np.load(os.path.join(DATA, "sample_embeddings.npy"))
print(f"Loaded {len(df):,} complaints and embeddings of shape {emb.shape}", flush=True)

# 2) CLUSTER: split the dots into N_THEMES crowds.
print(f"Clustering into {N_THEMES} themes...", flush=True)
km = KMeans(n_clusters=N_THEMES, random_state=RANDOM_SEED, n_init=10)
df["theme"] = km.fit_predict(emb)

# 3) DESCRIBE each theme with its most distinctive keywords.
#    TF-IDF = a score that highlights words common in THIS theme but rare overall.
vec = TfidfVectorizer(max_features=3000, stop_words="english", ngram_range=(1, 2))
tfidf = vec.fit_transform(df["narrative_clean"])
terms = np.array(vec.get_feature_names_out())

def top_keywords(theme_id, n=8):
    rows = np.where(df["theme"].values == theme_id)[0]
    mean_scores = np.asarray(tfidf[rows].mean(axis=0)).ravel()
    top_idx = mean_scores.argsort()[::-1][:n]
    return ", ".join(terms[top_idx])

# 4) Print a readable summary: size, keywords, and 1 example per theme.
print("\n" + "=" * 70)
print("THEMES FOUND (sorted by size)")
print("=" * 70)
sizes = df["theme"].value_counts()
for theme_id, count in sizes.items():
    pct = count / len(df) * 100
    print(f"\n### Theme {theme_id}  |  {count:,} complaints ({pct:.1f}%)")
    print("Top keywords:", top_keywords(theme_id))
    example = df[df["theme"] == theme_id]["narrative_clean"].iloc[0][:220]
    print("Example:", example, "...")

# 5) Save the clustered data for the next steps (naming + ranking).
df.to_parquet(os.path.join(DATA, "sample_clustered.parquet"), index=False)
print("\nSaved sample_clustered.parquet")
