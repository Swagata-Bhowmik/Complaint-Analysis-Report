<h1 align="center">🔍 Complaint Insight Engine</h1>

<p align="center">
  <b>Turn tens of thousands of raw customer complaints into a ranked, actionable list of the top problems — automatically.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue" />
  <img src="https://img.shields.io/badge/NLP-embeddings%20%2B%20clustering-6B8E23" />
  <img src="https://img.shields.io/badge/LLM-Gemini-8E44AD" />
  <img src="https://img.shields.io/badge/App-Streamlit-FF4B4B" />
  <img src="https://img.shields.io/badge/data-CFPB%20(public)-2C5C9E" />
  <img src="https://img.shields.io/badge/status-live%20%E2%9C%85-brightgreen" />
</p>

<p align="center">
  📓 <a href="project1_insight_engine/notebooks/insight_engine_full.ipynb"><b>Notebook</b></a> &nbsp;·&nbsp;
  🚀 <a href="https://complaint-insight-engine-swagata-bhowmik.streamlit.app"><b>Live App</b></a> &nbsp;·&nbsp;
  📊 <a href="https://swagata-bhowmik.github.io/Complaint-Insight-Engine/index.html"><b>Live Dashboard</b></a>
</p>

---

## 💡 What this does
Companies receive thousands of customer complaints in plain English — far too many for anyone to
read. This project uses **NLP** to automatically discover the **recurring problems** hidden in that
text and ranks them by **how common and how severe** they are — so a team knows exactly what to fix
first.

Built **end-to-end on real public data** (U.S. CFPB Consumer Complaint Database). No fabrication —
every number traces back to a real complaint and can be defended step by step.

---

## 🔗 Explore this project — 3 ways

<table>
<tr>
<td width="33%" valign="top">

### 📓 The Notebook
The **entire project in one file** — every step explained (blue / purple / green styled), runnable
code, and real interpreted outputs on the full 112k run.

➡️ [`insight_engine_full.ipynb`](project1_insight_engine/notebooks/insight_engine_full.ipynb)

</td>
<td width="33%" valign="top">

### 🚀 The Live App
An **interactive Streamlit dashboard** — walk the story chapter by chapter, then **upload your own
complaints file** and get instant ranked results.

➡️ [Open the Streamlit app ↗](https://complaint-insight-engine-swagata-bhowmik.streamlit.app)

</td>
<td width="33%" valign="top">

### 📊 The Dashboard
A fast, **always-on webpage** version of the whole project with a **searchable Q&A study page**.

➡️ [Open the dashboard ↗](https://swagata-bhowmik.github.io/Complaint-Insight-Engine/index.html)
&nbsp;·&nbsp; file: [`docs/index.html`](docs/index.html)

</td>
</tr>
</table>

> 💾 **Use the dashboard fully offline:** open [`docs/index.html`](docs/index.html) → **"Download raw file"** → open it in any browser.

---

## 🧠 How it works (the pipeline)

| Step | What happens | Tools |
|------|--------------|-------|
| 1️⃣ Ingest & clean | Chunked EDA on 8.5 GB, de-duplicate, normalize privacy masks, keep meaning | `pandas` · `regex` · `Parquet` |
| 2️⃣ Embed | Turn each complaint into a 384-dim meaning-vector | `sentence-transformers` (MiniLM) |
| 3️⃣ Cluster | Group similar complaints into themes (unsupervised) | `scikit-learn` (KMeans) |
| 4️⃣ Label | Extract each theme's distinctive keywords | `TF-IDF` |
| 5️⃣ Severity | Score negativity + high-stakes terms | `VADER` |
| 6️⃣ Prioritize | Rank by **Volume × Severity** | priority matrix |
| 7️⃣ Name | Give each theme a clear human label | `Google Gemini` (LLM) |
| 8️⃣ Deliver | Interactive dashboard + upload analyzer | `Streamlit` · `Plotly` |

---

## 📊 Key results — 112,481 credit-card complaints (2023–2026)

| # | Theme | Volume % | Severity | Priority |
|---|-------|:--------:|:--------:|:--------:|
| 🥇 1 | Unauthorized Charges & Fraud Disputes | 13.4 | 0.78 | 10.40 |
| 🥈 2 | Billing & Merchant Charge Disputes | 12.7 | 0.53 | 6.78 |
| 🥉 3 | Inaccurate Credit Reporting & Discrepancies | 8.8 | 0.46 | 4.07 |
| 4 | Payment Processing & Balance Errors | 11.2 | 0.34 | 3.85 |
| 5 | Unauthorized Credit-Card Applications | 9.7 | 0.37 | 3.62 |

**Headline:** fraud and disputes dominate — **#1 is both the most common *and* the most severe**, an
unambiguous "fix-first". Running on the full 112k (vs an 18k sample) produced **cleaner, more
distinct themes** — a real, documented finding. *(Full 12-theme table in the notebook.)*

---

## 🖥️ Run it locally

```bash
python -m venv .venv
.venv\Scripts\activate                                   # Windows
pip install -r project1_insight_engine/requirements.txt

# open the single end-to-end notebook...
jupyter notebook project1_insight_engine/notebooks/insight_engine_full.ipynb
# ...or launch the interactive dashboard
streamlit run project1_insight_engine/app/insight_app.py
```

---

## 🗂️ The data
**CFPB Consumer Complaint Database** — U.S. government open data (8.5 GB, 17.1M complaints, 3.8M with
narratives). Public, free, legally clean. Scope: credit-card complaints with a narrative, 2023
onward → 124,962 extracted → **112,481 after cleaning**. Chosen over app-store scraping (terms &
privacy risk). *Source: consumerfinance.gov/data-research/consumer-complaints.*

---

## 🛠️ Tech stack
`Python` · `pandas` · `Parquet` · `sentence-transformers (all-MiniLM-L6-v2)` · `scikit-learn (KMeans, TF-IDF, PCA)` ·
`VADER` · `Google Gemini (LLM)` · `Streamlit` · `Plotly` · `Git / GitHub`

---

## 🗺️ Roadmap
- [x] Data profiling & validation (17M-row source, chunked EDA)
- [x] Text cleaning (112k clean complaints)
- [x] NLP engine — embeddings → clustering → severity → priority → LLM naming
- [x] End-to-end analysis notebook (real 112k run, with outputs)
- [x] Interactive Streamlit dashboard + upload-and-analyze mode
- [x] Offline HTML dashboard with a Q&A study page
- [ ] Scheduled auto-refresh (GitHub Actions)

---
<p align="center"><i>Data science portfolio project by <b>Swagata Bhowmik</b> · built on real public data, defensible end-to-end.</i></p>
