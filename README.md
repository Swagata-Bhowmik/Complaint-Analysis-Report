# 🔍 Insight Engine — Mining Customer Complaints for the Top Problems to Fix

Turn tens of thousands of raw customer complaints into a **ranked, actionable list of the top
problems** — automatically — using NLP, clustering, sentiment-based severity, and an LLM, delivered
as an interactive web app.

> Built end-to-end on **real public data** (US CFPB Consumer Complaint Database). No fabrication —
> every result traces back to real complaints.

---

## What it does
1. **Ingests & cleans** raw complaint text (privacy-mask normalization, de-duplication).
2. **Embeds** each complaint into a meaning-vector (`sentence-transformers`, all-MiniLM-L6-v2).
3. **Clusters** similar complaints into themes (`KMeans`).
4. **Scores severity** (VADER sentiment + high-stakes keywords) and ranks by **priority = volume × severity**.
5. **Names** each theme with an LLM (Google Gemini).
6. **Delivers** it all in an interactive **Streamlit** dashboard — including an upload mode where
   anyone can analyze their own complaints file.

## Key results (112,481 credit-card complaints, 2023–2026)
- **#1 problem:** Unauthorized / fraudulent charges — the most common *and* most severe.
- Followed by merchant/refund disputes, credit-reporting issues, payment-processing errors,
  unauthorized applications, and identity theft.

## Tech stack
`Python` · `pandas` · `Parquet` · `sentence-transformers` · `scikit-learn` (KMeans, TF-IDF, PCA)
· `VADER` · `Google Gemini` · `Streamlit` · `Plotly`

## Project structure
```
project1_insight_engine/
  notebooks/    data profiling, cleaning, and the NLP engine (phase1-3 notebooks + scripts)
  app/          insight_app.py  — the interactive Streamlit dashboard
  outputs/      generated charts (priority matrix, theme sizes, meaning-map)
  README.md     detailed project write-up
  requirements.txt
```

## Run it locally
```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r project1_insight_engine/requirements.txt
streamlit run project1_insight_engine/app/insight_app.py
```
> The raw dataset and generated embeddings are not committed (large / re-downloadable). See
> `project1_insight_engine/README.md` for how to obtain the CFPB data.

---
*Data science portfolio project by Swagata Bhowmik.*
