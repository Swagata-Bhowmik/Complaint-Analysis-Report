# =============================================================================
# SCRIPT: build_severity.py
# GOAL:   Add a SEVERITY dimension to each theme and build a PRIORITY ranking.
#         Volume alone isn't enough - a business fixes problems that are both
#         COMMON and SEVERE first. This produces that "fix-first" list + a
#         priority-matrix chart.
#
# HOW WE MEASURE SEVERITY (two honest signals, combined):
#   1. NEGATIVITY: VADER sentiment on each complaint (lexicon-based, 0..1 where
#      1 = very negative). Angry/negative complaints score higher.
#   2. HIGH-STAKES WORDS: share of complaints mentioning serious issues
#      (fraud, unauthorized, stolen, scam, threat, legal, etc.).
#   theme_severity = average of (negativity) and (high-stakes share).
#
# PRIORITY SCORE = frequency_share(%) x theme_severity  -> rank themes by this.
#
# OUTPUTS: outputs/theme_priority.csv, outputs/priority_matrix.png
# =============================================================================

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "..", "outputs")

df = pd.read_parquet(os.path.join(DATA, "sample_clustered.parquet"))
print(f"Loaded {len(df):,} complaints", flush=True)

# --- 1) NEGATIVITY per complaint via VADER ---
# We score the ORIGINAL narrative (real words, not placeholders) for true tone.
analyzer = SentimentIntensityAnalyzer()
print("Scoring sentiment (negativity)...", flush=True)
# compound in [-1, 1]; convert to severity in [0, 1] where 1 = most negative.
comp = df["Consumer complaint narrative"].fillna("").apply(
    lambda t: analyzer.polarity_scores(t[:1000])["compound"]
)
df["negativity"] = (1 - comp) / 2  # -1 -> 1.0 (worst), +1 -> 0.0 (best)

# --- 2) HIGH-STAKES words flag per complaint ---
SEVERE = ["fraud", "unauthorized", "stolen", "steal", "scam", "theft",
          "identity", "threat", "lawsuit", "legal", "police", "victim",
          "hacked", "breach", "harass"]
pattern = "|".join(SEVERE)
df["severe_flag"] = df["Consumer complaint narrative"].str.contains(
    pattern, case=False, na=False
).astype(int)

# --- 3) Aggregate to theme level ---
# Recompute clean keyword names (same logic as build_themes).
NOISE = {"redacted", "date", "money", "xxxx", "xx", "account", "credit", "card",
         "credit card", "com", "www", "did", "told", "said"}
vec = TfidfVectorizer(max_features=4000, stop_words="english", ngram_range=(1, 2))
tfidf = vec.fit_transform(df["narrative_clean"]); terms = np.array(vec.get_feature_names_out())

def kws(tid, n=3):
    rows = np.where(df["theme"].values == tid)[0]
    order = np.asarray(tfidf[rows].mean(axis=0)).ravel().argsort()[::-1]
    out = []
    for i in order:
        w = terms[i]
        if w not in NOISE and not any(p in NOISE for p in w.split()):
            out.append(w)
        if len(out) == n:
            break
    return " / ".join(out).title()

g = df.groupby("theme")
theme = pd.DataFrame({
    "count": g.size(),
    "negativity": g["negativity"].mean(),
    "severe_share": g["severe_flag"].mean(),
})
theme["name"] = [kws(t) for t in theme.index]
theme["share_%"] = (theme["count"] / len(df) * 100).round(1)
# Combined severity = average of negativity and high-stakes share (both 0..1).
theme["severity"] = ((theme["negativity"] + theme["severe_share"]) / 2).round(3)
# Priority = how common x how severe.
theme["priority"] = (theme["share_%"] * theme["severity"]).round(2)

ranked = theme.sort_values("priority", ascending=False).reset_index()
ranked.insert(0, "rank", range(1, len(ranked) + 1))

print("\n" + "=" * 80)
print("PRIORITY RANKING  (fix-first = common AND severe)")
print("=" * 80)
for _, r in ranked.iterrows():
    print(f"#{r['rank']:>2}  priority={r['priority']:>5}  | {r['share_%']:>4}% vol | "
          f"severity={r['severity']:.2f} | {r['name']}")

ranked.to_csv(os.path.join(OUT, "theme_priority.csv"), index=False)
print("\nSaved outputs/theme_priority.csv")

# --- 4) PRIORITY MATRIX chart: x=volume, y=severity, bubble size=priority ---
plt.figure(figsize=(11, 7))
plt.scatter(ranked["share_%"], ranked["severity"],
            s=ranked["priority"] * 40, c=ranked["priority"], cmap="Reds",
            edgecolors="black", alpha=0.8)
for _, r in ranked.iterrows():
    plt.annotate(r["name"], (r["share_%"], r["severity"]),
                 fontsize=8, ha="center", va="center")
# quadrant guide lines at the medians.
plt.axvline(ranked["share_%"].median(), color="grey", ls="--", lw=0.8)
plt.axhline(ranked["severity"].median(), color="grey", ls="--", lw=0.8)
plt.title("Priority matrix: complaint themes (top-right = fix first)")
plt.xlabel("Volume  (% of complaints)")
plt.ylabel("Severity  (0-1, higher = more negative/serious)")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "priority_matrix.png"), dpi=120)
plt.close()
print("Saved outputs/priority_matrix.png")
print("\nDONE.")
