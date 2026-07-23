# =============================================================================
# MODULE: data_checks.py
# GOAL:   A REUSABLE data-validation toolkit. We run this after EVERY data
#         operation (loading, extracting, cleaning) to confirm the data is
#         sound BEFORE we act on it. This enforces our rule: "Don't just
#         perform the step - validate that the step did what we intended."
#
# WHY:    The data is the foundation. If it's wrong, missing, or corrupted,
#         everything built on it is wasted. This makes validation automatic,
#         thorough, and consistent - not something we forget.
#
# HOW TO USE (in a notebook):
#     from data_checks import validate
#     validate(df, text_col="Consumer complaint narrative",
#                  date_col="Date received", label_col="Product")
# =============================================================================

import pandas as pd


def validate(df, text_col=None, date_col=None, label_col=None, expected_cols=None):
    """Run a full validation report on a dataframe.

    Parameters
    ----------
    df           : the dataframe to check
    text_col     : (optional) the main text column to check for emptiness/length
    date_col     : (optional) a date column to check validity + range
    label_col    : (optional) a category column to check label consistency
    expected_cols: (optional) list of columns we REQUIRE to be present
    """
    print("=" * 64)
    print("DATA VALIDATION REPORT")
    print("=" * 64)

    # --- 1. SIZE ------------------------------------------------------------
    print(f"[1] SHAPE            : {df.shape[0]:,} rows  x  {df.shape[1]} columns")

    # --- 2. REQUIRED COLUMNS PRESENT ---------------------------------------
    if expected_cols:
        missing = [c for c in expected_cols if c not in df.columns]
        if missing:
            print(f"[2] REQUIRED COLUMNS : MISSING -> {missing}   FAIL")
        else:
            print(f"[2] REQUIRED COLUMNS : all present   OK")

    # --- 3. MISSING VALUES (nulls) -----------------------------------------
    null_pct = (df.isnull().mean() * 100).round(1).sort_values(ascending=False)
    worst = null_pct[null_pct > 0].head(5)
    print("[3] TOP MISSING %    :", dict(worst) if len(worst) else "no missing values")

    # --- 4. DUPLICATES ------------------------------------------------------
    dup = df.duplicated().sum()
    print(f"[4] DUPLICATE ROWS   : {dup:,}" + ("   (worth removing)" if dup else "   OK"))

    # --- 5. TEXT COLUMN CHECK ----------------------------------------------
    if text_col and text_col in df.columns:
        n_empty = df[text_col].isnull().sum()
        lengths = df[text_col].dropna().str.len()
        very_short = int((lengths < 20).sum())
        print(f"[5] TEXT '{text_col[:22]}...' : "
              f"empty={n_empty:,}, median_len={int(lengths.median())} chars, "
              f"very_short(<20)={very_short:,}")

    # --- 6. DATE COLUMN CHECK ----------------------------------------------
    if date_col and date_col in df.columns:
        d = pd.to_datetime(df[date_col], errors="coerce")
        n_bad = d.isnull().sum()
        status = "OK" if n_bad == 0 else f"{n_bad:,} INVALID   CHECK!"
        print(f"[6] DATE '{date_col}' : range {d.min()} -> {d.max()} | invalid={status}")

    # --- 7. LABEL CONSISTENCY ----------------------------------------------
    if label_col and label_col in df.columns:
        vc = df[label_col].value_counts()
        print(f"[7] LABELS '{label_col}' : {len(vc)} distinct ->")
        for name, cnt in vc.items():
            print(f"        {cnt:>8,}  |  {name}")

    print("=" * 64)
    print("Review each line above. Anything marked FAIL/CHECK must be fixed before moving on.")
    print("=" * 64)
