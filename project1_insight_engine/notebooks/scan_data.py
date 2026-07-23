# =============================================================================
# SCRIPT: scan_data.py
# GOAL:   Understand the FULL CFPB dataset (8.5 GB) WITHOUT loading it all into
#         memory at once. We read it in "chunks" (small batches of rows) and
#         accumulate summary numbers. This is the professional way to profile
#         data that is bigger than your RAM.
#
# WHAT IT MEASURES (the questions we must answer before building):
#   1. Total number of complaints (rows).
#   2. How many have a written narrative (the text our engine needs).
#   3. The date range (earliest and latest complaint).
#   4. How narratives are distributed by YEAR (to see when text data is available).
#   5. The top PRODUCTS (so we can choose our scope sensibly).
#
# HOW TO READ THE OUTPUT: printed at the bottom as a clear summary.
# =============================================================================

import pandas as pd

# Path to the full raw file the user downloaded.
FILE = r"C:\Users\Lenovo\Downloads\PROJECTS\complaints.csv\complaints.csv"

# We only need a few columns for profiling -> reading fewer columns = faster + lighter.
COLS = ["Date received", "Product", "Consumer complaint narrative", "Company"]

# CHUNK SIZE: how many rows we load at a time. 200,000 rows fit easily in RAM.
CHUNK = 200_000

# --- Accumulators: running totals we update as we walk through the file ---
total_rows = 0
total_narr = 0
year_counts = {}
year_narr_counts = {}
product_narr_counts = {}
min_date = None
max_date = None

print("Scanning the full file in chunks... (this takes a couple of minutes)\n", flush=True)

reader = pd.read_csv(FILE, usecols=COLS, chunksize=CHUNK, low_memory=False)

for i, chunk in enumerate(reader):
    total_rows += len(chunk)

    has_narr = chunk["Consumer complaint narrative"].notna()
    total_narr += int(has_narr.sum())

    # utc=True makes ALL dates timezone-aware consistently, then we drop the tz
    # so every date is compared on the same simple basis (fixes tz-naive vs tz-aware error).
    dates = pd.to_datetime(chunk["Date received"], errors="coerce", utc=True).dt.tz_localize(None)
    years = dates.dt.year

    cmin, cmax = dates.min(), dates.max()
    if pd.notna(cmin):
        min_date = cmin if min_date is None else min(min_date, cmin)
    if pd.notna(cmax):
        max_date = cmax if max_date is None else max(max_date, cmax)

    for y, cnt in years.value_counts().items():
        year_counts[y] = year_counts.get(y, 0) + int(cnt)
    for y, cnt in years[has_narr].value_counts().items():
        year_narr_counts[y] = year_narr_counts.get(y, 0) + int(cnt)

    for p, cnt in chunk.loc[has_narr, "Product"].value_counts().items():
        product_narr_counts[p] = product_narr_counts.get(p, 0) + int(cnt)

    if (i + 1) % 10 == 0:
        print(f"  ...processed {total_rows:,} rows so far", flush=True)

print("\n" + "=" * 70)
print("DATA PROFILE - FULL CFPB FILE")
print("=" * 70)
print(f"Total complaints (rows)        : {total_rows:,}")
print(f"Complaints WITH narrative text : {total_narr:,}  "
      f"({round(total_narr/total_rows*100,1)}% of all)")
print(f"Date range                     : {min_date.date()}  ->  {max_date.date()}")

print("\n--- Narratives available BY YEAR (the text we can actually use) ---")
for y in sorted(year_narr_counts):
    all_y = year_counts.get(y, 0)
    narr_y = year_narr_counts.get(y, 0)
    pct = round(narr_y / all_y * 100, 1) if all_y else 0
    print(f"  {int(y)} : {narr_y:>9,} narratives   (out of {all_y:>9,} total = {pct}%)")

print("\n--- TOP 12 PRODUCTS by number of complaints WITH narrative ---")
top = sorted(product_narr_counts.items(), key=lambda kv: kv[1], reverse=True)[:12]
for p, cnt in top:
    print(f"  {cnt:>9,}  |  {p}")

print("\nScan complete.")
