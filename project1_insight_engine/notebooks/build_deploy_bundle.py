# =============================================================================
# SCRIPT: build_deploy_bundle.py
# GOAL:   Create a SMALL bundle the deployed (hosted) app can read from GitHub —
#         the ranked themes + a few real example complaints per theme.
#         The full 112k data stays local; this bundle is tiny and committable.
#
# OUTPUT: project1_insight_engine/app/deploy_data.json
# =============================================================================

import os, json
import pandas as pd

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "data")
APP = os.path.join(HERE, "..", "app")

themes = pd.read_csv(os.path.join(DATA, "..", "outputs", "theme_final_full.csv")).sort_values("rank")
clustered = pd.read_parquet(os.path.join(DATA, "full_clustered.parquet"))

bundle = {
    "total_complaints": int(len(clustered)),
    "n_themes": int(themes["theme"].nunique()),
    "themes": [],
}

for _, r in themes.iterrows():
    tid = int(r["theme"])
    # up to 3 real example complaints, trimmed for size
    examples = (clustered[clustered["theme"] == tid]["Consumer complaint narrative"]
                .head(3).astype(str).apply(lambda t: t[:400]).tolist())
    bundle["themes"].append({
        "rank": int(r["rank"]),
        "theme": tid,
        "name": str(r["name"]),
        "description": str(r["description"]),
        "share_pct": float(r["share_%"]),
        "severity": float(r["severity"]),
        "priority": float(r["priority"]),
        "examples": examples,
    })

out = os.path.join(APP, "deploy_data.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)

size_kb = round(os.path.getsize(out) / 1024, 1)
print(f"Wrote {out}  ({size_kb} KB, {bundle['n_themes']} themes, "
      f"{bundle['total_complaints']:,} complaints represented)")
