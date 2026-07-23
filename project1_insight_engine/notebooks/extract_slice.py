# =============================================================================
# SCRIPT: extract_slice.py  (v2 - FIXED)
# GOAL:   Carve a small, clean WORKING SLICE out of the huge 8.5 GB raw file
#         and save it SAFELY as Parquet (not CSV).
#
# WHY v2: v1 saved to CSV via repeated appends. The complaint narratives contain
#         commas, quotes, and LINE BREAKS, which corrupted the CSV structure
#         (124,962 rows but only ~6,281 had valid dates - the rest were mangled).
#         LESSON: CSV is fragile for free text. Parquet stores text safely,
#         is smaller, faster, and preserves data types.
#
# OUR SCOPE (locked with the user):
#   - Product   : Credit card  (merging the two label variants)
#   - Has text  : only rows WITH a written consumer narrative
#   - Time range: 2023-01-01 onward
#
# METHOD: read the big file in memory-safe CHUNKS, filter each chunk, collect the
#         keeper chunks in a list, concatenate once, and write a single Parquet file.
#
# OUTPUT: project1_insight_engine/data/creditcard_complaints.parquet
# =============================================================================

import pandas as pd
import os

RAW_FILE = r"C:\Users\Lenovo\Downloads\PROJECTS\complaints.csv\complaints.csv"
OUT_FILE = r"C:\Users\Lenovo\Downloads\PROJECTS\project1_insight_engine\data\creditcard_complaints.parquet"

PRODUCT_KEYWORDS = ["credit card"]     # matches "Credit card" AND "Credit card or prepaid card"
START_DATE = "2023-01-01"
CHUNK = 200_000

keepers = []          # list of filtered chunks; concatenated once at the end
kept_total = 0

print("Extracting credit-card complaints (2023+, with narrative) -> Parquet...\n", flush=True)

reader = pd.read_csv(RAW_FILE, chunksize=CHUNK, low_memory=False)

for i, chunk in enumerate(reader):
    # 1) Must have narrative text.
    m_text = chunk["Consumer complaint narrative"].notna()

    # 2) Product contains "credit card" (case-insensitive).
    prod = chunk["Product"].str.lower()
    m_prod = prod.str.contains("credit card", na=False)

    # 3) Date on/after START_DATE (normalize timezones).
    dates = pd.to_datetime(chunk["Date received"], errors="coerce", utc=True).dt.tz_localize(None)
    m_date = dates >= pd.Timestamp(START_DATE)

    keep = chunk[m_text & m_prod & m_date].copy()
    if len(keep) > 0:
        # Convert the date INSIDE each chunk (proven to work per-chunk). Storing a
        # proper datetime here prevents type-mixing when chunks are concatenated.
        keep["Date received"] = dates[m_text & m_prod & m_date].values
        keepers.append(keep)
        kept_total += len(keep)

    if (i + 1) % 10 == 0:
        print(f"  ...scanned {(i+1)*CHUNK:,} rows, kept {kept_total:,} so far", flush=True)

# Concatenate all keeper chunks into one dataframe, then write ONE parquet file.
# Dates were already converted per-chunk, so concat preserves them correctly.
result = pd.concat(keepers, ignore_index=True)

result.to_parquet(OUT_FILE, index=False)

size_mb = round(os.path.getsize(OUT_FILE) / 1048576, 1)
print("\n" + "=" * 60)
print("EXTRACTION COMPLETE (Parquet)")
print("=" * 60)
print(f"Rows kept: {kept_total:,}")
print(f"Valid dates: {result['Date received'].notna().sum():,}")
print(f"Year distribution:")
print(result['Date received'].dt.year.value_counts().sort_index().to_string())
print(f"\nSaved to: {OUT_FILE}")
print(f"Size: {size_mb} MB")
