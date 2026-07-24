# =============================================================================
# SCRIPT: scale_embeddings.py
# GOAL:   Embed the FULL cleaned dataset (~112k complaints) and save the vectors.
#         This is the long step (~75 min on CPU). We save so it's done ONCE.
#
# NOTE:   Saved separately from analysis so an interruption later never wastes
#         this expensive computation. Run this, then run analyze_full.py.
#
# OUTPUT: data/full_complaints.parquet   (all cleaned complaints)
#         data/full_embeddings.npy        (their 384-dim meaning-vectors)
# =============================================================================

import os, time
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "data")
MODEL_NAME = "all-MiniLM-L6-v2"

# Load ALL cleaned complaints (not a sample this time).
df = pd.read_parquet(os.path.join(DATA, "creditcard_clean.parquet")).reset_index(drop=True)
print(f"Embedding ALL {len(df):,} complaints. This is the long run (~75 min).", flush=True)

model = SentenceTransformer(MODEL_NAME)

t0 = time.time()
embeddings = model.encode(
    df["narrative_clean"].tolist(),
    show_progress_bar=True,
    batch_size=32,
)
print(f"Done in {(time.time()-t0)/60:.1f} min. Shape: {embeddings.shape}", flush=True)

df.to_parquet(os.path.join(DATA, "full_complaints.parquet"), index=False)
np.save(os.path.join(DATA, "full_embeddings.npy"), embeddings)
print("Saved full_complaints.parquet and full_embeddings.npy", flush=True)
