# =============================================================================
# SCRIPT: build_embeddings.py
# GOAL:   Convert complaint text into EMBEDDINGS (meaning-vectors) and SAVE them,
#         so the expensive computation is done ONCE and reused instantly later.
#
# WHAT IS AN EMBEDDING? A fixed-length list of numbers that captures the MEANING
#         of a piece of text. Texts with similar meaning get similar vectors.
#         We use the model 'all-MiniLM-L6-v2' -> each complaint becomes 384 numbers.
#         Think of it as a GPS coordinate in "meaning space": similar complaints
#         land near each other, which is what lets us cluster them into themes.
#
# WHY SAVE THEM? Embedding is slow on CPU (~12 min for 18k). We compute once,
#         save to disk, then the notebook reloads them in a second for all the
#         clustering / naming / ranking experiments.
#
# STRATEGY: prototype on a SAMPLE first (default 18,000), then scale to all later.
#
# OUTPUT: data/sample_complaints.parquet   (the sampled rows we embedded)
#         data/sample_embeddings.npy       (the matching meaning-vectors)
# =============================================================================

import sys, os, time
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "data")

SAMPLE_SIZE = 18_000        # how many complaints to prototype on
RANDOM_SEED = 42            # fixed seed -> reproducible sample
MODEL_NAME = "all-MiniLM-L6-v2"

# 1) Load cleaned data and take a reproducible random sample.
df = pd.read_parquet(os.path.join(DATA, "creditcard_clean.parquet"))
sample = df.sample(n=min(SAMPLE_SIZE, len(df)), random_state=RANDOM_SEED).reset_index(drop=True)
print(f"Sampled {len(sample):,} complaints (seed={RANDOM_SEED}).", flush=True)

# 2) Load the embedding model.
print(f"Loading model {MODEL_NAME}...", flush=True)
model = SentenceTransformer(MODEL_NAME)

# 3) Embed the cleaned narratives.
print("Embedding... (this takes ~12 min on CPU for 18k)", flush=True)
t0 = time.time()
embeddings = model.encode(
    sample["narrative_clean"].tolist(),
    show_progress_bar=True,
    batch_size=32,
)
print(f"Done in {(time.time()-t0)/60:.1f} min. Shape: {embeddings.shape}", flush=True)

# 4) Save both the sample rows and their embeddings (aligned by row order).
sample.to_parquet(os.path.join(DATA, "sample_complaints.parquet"), index=False)
np.save(os.path.join(DATA, "sample_embeddings.npy"), embeddings)
print("Saved sample_complaints.parquet and sample_embeddings.npy", flush=True)
