# =============================================================================
# SCRIPT: name_themes_llm.py
# GOAL:   Use the Gemini AI to give each theme a crisp, professional NAME and a
#         one-line DESCRIPTION, based on its keywords + real example complaints.
#         This replaces clunky keyword-joins like "Company / Received / Payment"
#         with human names like "Billing and customer-service problems".
#
# HOW IT WORKS:
#   - For each theme: gather top keywords + 3 real complaint snippets.
#   - Ask Gemini to return a short name (<=6 words) + a one-line description.
#   - Merge the AI names into our priority table and save the final result.
#
# SAFE: the API key is read from the .env file (never hard-coded, never pushed).
# COST: ~12 tiny calls on the free tier. If a call fails, we fall back to keywords.
#
# OUTPUT: outputs/theme_final.csv  (rank, ai_name, description, volume, severity, priority)
# =============================================================================

import os, time, json
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from google import genai
from sklearn.feature_extraction.text import TfidfVectorizer

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "..", "outputs")

MODEL = "gemini-flash-lite-latest"

# --- Load clustered data + the priority table we already computed ---
df = pd.read_parquet(os.path.join(DATA, "sample_clustered.parquet"))
priority = pd.read_csv(os.path.join(OUT, "theme_priority.csv"))
print(f"Loaded {len(df):,} complaints and {len(priority)} themes", flush=True)

# --- Keyword helper (clean, reused) ---
NOISE = {"redacted", "date", "money", "xxxx", "xx", "account", "credit", "card",
         "credit card", "com", "www", "did", "told", "said"}
vec = TfidfVectorizer(max_features=4000, stop_words="english", ngram_range=(1, 2))
tfidf = vec.fit_transform(df["narrative_clean"]); terms = np.array(vec.get_feature_names_out())

def keywords_for(theme_id, n=8):
    rows = np.where(df["theme"].values == theme_id)[0]
    order = np.asarray(tfidf[rows].mean(axis=0)).ravel().argsort()[::-1]
    out = []
    for i in order:
        w = terms[i]
        if w not in NOISE and not any(p in NOISE for p in w.split()):
            out.append(w)
        if len(out) == n:
            break
    return out

def examples_for(theme_id, n=3):
    texts = df[df["theme"] == theme_id]["Consumer complaint narrative"].head(n).tolist()
    return [t[:300] for t in texts]

# --- Connect to Gemini ---
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(theme_id):
    kws = ", ".join(keywords_for(theme_id))
    exs = "\n".join(f"- {e}" for e in examples_for(theme_id))
    prompt = (
        "You are analyzing customer credit-card complaints. Based on the keywords and "
        "example complaints below, give a SHORT theme name (max 6 words) and a one-line "
        "description of the problem. Respond ONLY as JSON: "
        '{"name": "...", "description": "..."}\n\n'
        f"Keywords: {kws}\n\nExamples:\n{exs}"
    )
    resp = client.models.generate_content(model=MODEL, contents=prompt)
    text = resp.text.strip()
    # Strip code fences if present.
    if text.startswith("```"):
        text = text.strip("`").split("\n", 1)[-1].rsplit("```", 1)[0]
    try:
        data = json.loads(text)
        return data.get("name", ""), data.get("description", "")
    except Exception:
        return "", text[:120]

# --- Name each theme ---
names, descs = {}, {}
for tid in sorted(df["theme"].unique()):
    try:
        name, desc = ask_gemini(tid)
        if not name:
            name = " / ".join(keywords_for(tid, 3)).title()
        names[tid] = name
        descs[tid] = desc
        print(f"Theme {tid}: {name}  ->  {desc[:70]}", flush=True)
    except Exception as e:
        names[tid] = " / ".join(keywords_for(tid, 3)).title()
        descs[tid] = f"(AI failed: {type(e).__name__}) keywords used"
        print(f"Theme {tid}: fallback ({type(e).__name__})", flush=True)
    time.sleep(1)  # gentle pacing for the free tier

# --- Merge AI names into the priority table + save ---
priority["ai_name"] = priority["theme"].map(names)
priority["description"] = priority["theme"].map(descs)
cols = ["rank", "ai_name", "description", "share_%", "severity", "priority"]
final = priority[cols].sort_values("rank")
final.to_csv(os.path.join(OUT, "theme_final.csv"), index=False)

print("\n" + "=" * 78)
print("FINAL NAMED & RANKED THEMES")
print("=" * 78)
for _, r in final.iterrows():
    print(f"#{r['rank']:>2} [{r['priority']:>5}] {r['ai_name']}")
    print(f"     {r['description']}")
print("\nSaved outputs/theme_final.csv")
