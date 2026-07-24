# =============================================================================
# SCRIPT: analyze_full.py
# GOAL:   Run the full analysis on the FULL 112k embeddings (already saved):
#         cluster -> severity -> priority -> AI-name -> save results + charts.
#         Fast (~2 min + 12 quick AI calls). Run AFTER scale_embeddings.py.
#
# OUTPUTS: outputs/theme_final_full.csv
#          outputs/priority_matrix_full.png
#          outputs/theme_sizes_full.png
#          data/full_clustered.parquet
# =============================================================================

import os, time, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
from google import genai

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "..", "outputs")
N_THEMES = 12
MODEL = "gemini-flash-lite-latest"

# --- Load full data + embeddings ---
df = pd.read_parquet(os.path.join(DATA, "full_complaints.parquet")).reset_index(drop=True)
emb = np.load(os.path.join(DATA, "full_embeddings.npy"))
print(f"Loaded {len(df):,} complaints, embeddings {emb.shape}", flush=True)

# --- 1) Cluster ---
print("Clustering...", flush=True)
km = KMeans(n_clusters=N_THEMES, random_state=42, n_init=10)
df["theme"] = km.fit_predict(emb)

# --- 2) Severity (VADER negativity + high-stakes words) ---
print("Scoring severity...", flush=True)
analyzer = SentimentIntensityAnalyzer()
comp = df["Consumer complaint narrative"].fillna("").apply(
    lambda t: analyzer.polarity_scores(t[:1000])["compound"])
df["negativity"] = (1 - comp) / 2
SEVERE = ["fraud", "unauthorized", "stolen", "steal", "scam", "theft",
          "identity", "threat", "lawsuit", "legal", "police", "victim"]
df["severe_flag"] = df["Consumer complaint narrative"].str.contains(
    "|".join(SEVERE), case=False, na=False).astype(int)

# --- 3) Keywords per theme ---
NOISE = {"redacted", "date", "money", "xxxx", "xx", "account", "credit", "card",
         "credit card", "com", "www", "did", "told", "said"}
vec = TfidfVectorizer(max_features=4000, stop_words="english", ngram_range=(1, 2))
tfidf = vec.fit_transform(df["narrative_clean"]); terms = np.array(vec.get_feature_names_out())

def keywords_for(tid, n=8):
    rows = np.where(df["theme"].values == tid)[0]
    order = np.asarray(tfidf[rows].mean(axis=0)).ravel().argsort()[::-1]
    out = []
    for i in order:
        w = terms[i]
        if w not in NOISE and not any(p in NOISE for p in w.split()):
            out.append(w)
        if len(out) == n:
            break
    return out

# --- 4) Priority table ---
g = df.groupby("theme")
theme = pd.DataFrame({
    "count": g.size(),
    "severity": ((g["negativity"].mean() + g["severe_flag"].mean()) / 2).round(3),
})
theme["share_%"] = (theme["count"] / len(df) * 100).round(1)
theme["priority"] = (theme["share_%"] * theme["severity"]).round(2)
theme = theme.sort_values("priority", ascending=False).reset_index()
theme.insert(0, "rank", range(1, len(theme) + 1))

# --- 5) AI names ---
print("Naming themes with Gemini...", flush=True)
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ai_name(tid):
    kws = ", ".join(keywords_for(tid))
    exs = "\n".join(f"- {t[:300]}" for t in
                    df[df["theme"] == tid]["Consumer complaint narrative"].head(3))
    prompt = ("You are analyzing customer credit-card complaints. Based on the keywords and "
              "examples, give a SHORT theme name (max 6 words) and one-line description. "
              'Respond ONLY as JSON: {"name":"...","description":"..."}\n\n'
              f"Keywords: {kws}\n\nExamples:\n{exs}")
    try:
        text = client.models.generate_content(model=MODEL, contents=prompt).text.strip()
        if text.startswith("```"):
            text = text.strip("`").split("\n", 1)[-1].rsplit("```", 1)[0]
        d = json.loads(text)
        return d.get("name", ""), d.get("description", "")
    except Exception as e:
        return " / ".join(keywords_for(tid, 3)).title(), f"(AI fallback: {type(e).__name__})"

names, descs = {}, {}
for tid in sorted(df["theme"].unique()):
    n, d = ai_name(tid)
    names[tid], descs[tid] = n, d
    print(f"  theme {tid}: {n}", flush=True)
    time.sleep(1)

theme["name"] = theme["theme"].map(names)
theme["description"] = theme["theme"].map(descs)

# --- Save results ---
theme.to_csv(os.path.join(OUT, "theme_final_full.csv"), index=False)
df.to_parquet(os.path.join(DATA, "full_clustered.parquet"), index=False)

print("\n" + "=" * 78)
print("FULL DATASET - TOP PROBLEMS (112k complaints)")
print("=" * 78)
for _, r in theme.iterrows():
    print(f"#{r['rank']:>2} [{r['priority']:>5}] {r['name']}  ({r['share_%']}% vol, sev {r['severity']})")

# --- Charts ---
s = theme.sort_values("count")
plt.figure(figsize=(10, 6))
plt.barh(s["name"], s["count"], color="#4C72B0")
plt.title("Credit-card complaint themes by volume (FULL 112k)")
plt.xlabel("Number of complaints"); plt.tight_layout()
plt.savefig(os.path.join(OUT, "theme_sizes_full.png"), dpi=120); plt.close()

plt.figure(figsize=(11, 7))
plt.scatter(theme["share_%"], theme["severity"], s=theme["priority"] * 40,
            c=theme["priority"], cmap="Reds", edgecolors="black", alpha=0.8)
for _, r in theme.iterrows():
    plt.annotate(str(r["name"]), (r["share_%"], r["severity"]), fontsize=8, ha="center")
plt.axvline(theme["share_%"].median(), color="grey", ls="--", lw=0.8)
plt.axhline(theme["severity"].median(), color="grey", ls="--", lw=0.8)
plt.title("Priority matrix - FULL 112k credit-card complaints")
plt.xlabel("Volume (% of complaints)"); plt.ylabel("Severity (0-1)")
plt.tight_layout(); plt.savefig(os.path.join(OUT, "priority_matrix_full.png"), dpi=120); plt.close()

print("\nSaved theme_final_full.csv, theme_sizes_full.png, priority_matrix_full.png, full_clustered.parquet")
