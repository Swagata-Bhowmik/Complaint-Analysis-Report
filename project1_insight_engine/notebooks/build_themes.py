# =============================================================================
# SCRIPT: build_themes.py
# GOAL:   Turn raw clusters into a clean, named, RANKED list of problems, plus
#         two pictures: theme sizes and a 2D "meaning map" of the clusters.
#
# STEPS (all fast - reuses saved embeddings + clusters):
#   1. Clean the keyword labels (drop privacy-placeholder noise words).
#   2. Auto-name each theme from its top clean keywords.
#   3. Rank themes by how many complaints they contain (frequency).
#   4. Save a tidy themes table (outputs/theme_summary.csv).
#   5. Chart A: bar chart of theme sizes (outputs/theme_sizes.png).
#   6. Chart B: 2D map of the clusters via PCA (outputs/theme_map.png).
# =============================================================================

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # save charts to files without needing a screen
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "..", "outputs")
os.makedirs(OUT, exist_ok=True)

# Load clustered complaints and their embeddings.
df = pd.read_parquet(os.path.join(DATA, "sample_clustered.parquet"))
emb = np.load(os.path.join(DATA, "sample_embeddings.npy"))
print(f"Loaded {len(df):,} complaints across {df['theme'].nunique()} themes", flush=True)

# 1) Extra stopwords = privacy placeholders + generic filler that add no meaning.
NOISE = ["redacted", "date", "money", "xxxx", "xx", "account", "credit", "card",
         "credit card", "com", "www", "did", "told", "said"]
stopwords = "english"
vec = TfidfVectorizer(max_features=4000, stop_words=stopwords,
                      ngram_range=(1, 2))
tfidf = vec.fit_transform(df["narrative_clean"])
terms = np.array(vec.get_feature_names_out())
noise_set = set(NOISE)

def top_keywords(theme_id, n=6):
    rows = np.where(df["theme"].values == theme_id)[0]
    scores = np.asarray(tfidf[rows].mean(axis=0)).ravel()
    order = scores.argsort()[::-1]
    kws = []
    for i in order:
        w = terms[i]
        if w not in noise_set and not any(part in noise_set for part in w.split()):
            kws.append(w)
        if len(kws) == n:
            break
    return kws

# 2) Build a readable name from the top 3 clean keywords.
def theme_name(theme_id):
    kws = top_keywords(theme_id, n=3)
    return " / ".join(kws).title() if kws else f"Theme {theme_id}"

# 3) Build the ranked themes table.
rows = []
for theme_id, count in df["theme"].value_counts().items():
    rows.append({
        "theme_id": theme_id,
        "name": theme_name(theme_id),
        "count": int(count),
        "share_%": round(count / len(df) * 100, 1),
        "keywords": ", ".join(top_keywords(theme_id, 6)),
    })
summary = pd.DataFrame(rows).sort_values("count", ascending=False).reset_index(drop=True)
summary.insert(0, "rank", range(1, len(summary) + 1))

print("\n" + "=" * 74)
print("RANKED THEMES (top problems by volume)")
print("=" * 74)
for _, r in summary.iterrows():
    print(f"#{r['rank']:>2}  {r['count']:>5,} ({r['share_%']:>4}%)  {r['name']}")
    print(f"        keywords: {r['keywords']}")

summary.to_csv(os.path.join(OUT, "theme_summary.csv"), index=False)
print("\nSaved outputs/theme_summary.csv")

# 5) Chart A: theme sizes (horizontal bar, biggest on top).
plt.figure(figsize=(10, 6))
s = summary.sort_values("count")
plt.barh(s["name"], s["count"], color="#4C72B0")
plt.title("Credit-card complaint themes by volume (18k sample)")
plt.xlabel("Number of complaints")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "theme_sizes.png"), dpi=120)
plt.close()
print("Saved outputs/theme_sizes.png")

# 6) Chart B: 2D "meaning map" of the clusters (PCA squashes 384 dims -> 2).
print("Building 2D meaning-map (PCA)...", flush=True)
coords = PCA(n_components=2, random_state=42).fit_transform(emb)
plt.figure(figsize=(9, 7))
scatter = plt.scatter(coords[:, 0], coords[:, 1], c=df["theme"], cmap="tab20", s=4, alpha=0.5)
plt.title("Meaning-map of complaints (each dot = 1 complaint, color = theme)")
plt.xlabel("dimension 1"); plt.ylabel("dimension 2")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "theme_map.png"), dpi=120)
plt.close()
print("Saved outputs/theme_map.png")
print("\nDONE.")
