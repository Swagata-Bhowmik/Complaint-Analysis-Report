# =============================================================================
# MODULE: text_cleaning.py
# GOAL:   Reusable functions to CLEAN the CFPB complaint narratives so they are
#         ready for NLP, WITHOUT destroying meaning.
#
# WHY:    Raw narratives contain CFPB privacy "masks" that are noise to a model:
#           - "XXXX"            -> redacted names/companies/account numbers
#           - "XX/XX/year>"     -> redacted dates (a scrubbing artifact)
#           - "{$70.00}"        -> redacted money amounts wrapped in braces
#         Left raw, these confuse theme-finding. Removed too aggressively, we
#         lose the real words. So we replace masks with NEUTRAL placeholders /
#         remove the noise while keeping the surrounding real sentence intact.
#
# DESIGN: we KEEP the original text and add a separate cleaned column, so we can
#         always show before/after and never lose the raw data.
# =============================================================================

import re
import pandas as pd

# Product labels that mean the same thing -> merge into one canonical label.
PRODUCT_CANONICAL = {
    "Credit card": "Credit card",
    "Credit card or prepaid card": "Credit card",
}


def clean_narrative(text: str) -> str:
    """Clean ONE narrative string. Returns a tidy, model-ready version.

    Steps (order matters):
      1. Replace redacted DATE patterns 'XX/XX/year>' (and variants) with ' <date> '.
      2. Replace redacted MONEY '{$123.45}' with ' <money> '.
      3. Replace runs of X-masks (XXXX, XX, XXXXX...) with ' <redacted> '.
      4. Collapse repeated placeholders and extra whitespace.
    """
    if not isinstance(text, str):
        return ""

    t = text

    # 1) Redacted dates: things like "XX/XX/year>", "XX/XX/XXXX", "XX/XX/2024".
    t = re.sub(r"XX/XX/(year>|\d{2,4}|XXXX)", " <date> ", t)

    # 2) Redacted money amounts wrapped in braces: {$70.00}, {$1,200}.
    t = re.sub(r"\{\$[\d,\.]*\}", " <money> ", t)

    # 3) Any remaining run of 2+ capital X's (redacted names/accounts/companies).
    t = re.sub(r"X{2,}", " <redacted> ", t)

    # 4) Collapse repeated placeholders e.g. "<redacted> <redacted>" -> one.
    t = re.sub(r"(<redacted>\s*){2,}", "<redacted> ", t)
    t = re.sub(r"(<date>\s*){2,}", "<date> ", t)

    # 5) Normalize whitespace (newlines/tabs/multiple spaces -> single space).
    t = re.sub(r"\s+", " ", t).strip()

    return t


def clean_dataframe(df: pd.DataFrame,
                    text_col: str = "Consumer complaint narrative",
                    product_col: str = "Product",
                    min_chars: int = 50) -> pd.DataFrame:
    """Apply the full Phase-2 cleaning pipeline to the dataframe.

    Returns a NEW dataframe with:
      - merged/canonical product labels (in a new column 'product_clean')
      - a new 'narrative_clean' column (original text kept intact)
      - exact-duplicate narratives removed
      - very short narratives (< min_chars of ORIGINAL text) removed
    """
    out = df.copy()

    # a) Merge product labels into a single canonical category.
    out["product_clean"] = out[product_col].map(PRODUCT_CANONICAL).fillna(out[product_col])

    # b) Drop exact-duplicate narratives (keep the first occurrence).
    before = len(out)
    out = out.drop_duplicates(subset=[text_col]).copy()
    dropped_dups = before - len(out)

    # c) Drop very-short narratives (based on ORIGINAL text length).
    before2 = len(out)
    out = out[out[text_col].str.len() >= min_chars].copy()
    dropped_short = before2 - len(out)

    # d) Build the cleaned narrative column.
    out["narrative_clean"] = out[text_col].apply(clean_narrative)

    # Attach simple stats as attributes for reporting.
    out.attrs["dropped_duplicates"] = dropped_dups
    out.attrs["dropped_short"] = dropped_short

    return out
