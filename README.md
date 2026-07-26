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
  🚀 <a href="https://complaint-insight-engine-swagata-bhowmik.streamlit.app"><b>Live Interactive App</b></a> &nbsp;·&nbsp;
  📊 <a href="https://swagata-bhowmik.github.io/Complaint-Insight-Engine/"><b>Live Dashboard (always-on)</b></a>
</p>

---

## 💡 What this does
Companies receive thousands of customer complaints in plain English — far too many for anyone to
read. This project uses **NLP** to automatically discover the **recurring problems** hidden in that
text and ranks them by **how common and how severe** they are — so a team knows exactly what to fix
first.

Built **end-to-end on real public data** (US CFPB Consumer Complaint Database). No fabrication —
every number traces back to a real complaint and can be defended step by step.

---

## 🔗 Explore this project (3 ways)

| | What | Link |
|---|------|------|
| 📓 | **The full analysis notebook** — every step explained with theory, colorful markdown, runnable code & interpreted outputs (the real 112k run) | [`notebooks/phase3_full_depth.ipynb`](project1_insight_engine/notebooks/phase3_full_depth.ipynb) |
| 🚀 | **Live interactive app** — walk the story + upload your OWN complaints file and get instant results | [Open the Streamlit app ↗](https://complaint-insight-engine-swagata-bhowmik.streamlit.app) |
| 📊 | **Live HTML dashboard** — a fast, always-on webpage version (never sleeps); also downloadable from [`docs/index.html`](docs/index.html) | [Open the dashboard ↗](https://swagata-bhowmik.github.io/Complaint-Insight-Engine/) |

> 💾 **Download the HTML dashboard:** open [`docs/index.html`](docs/index.html) → click the **"Download raw file"** button on GitHub → open it in any browser, fully offline.

---

## 🧠 How it works (the pipeline)

| Step | What happens | Tools |
|------|--------------|-------|
| 1️⃣ Ingest & clean | De-duplicate, normalize privacy masks, keep meaning | `pandas`, `regex`, `Parquet` |
| 2️⃣ Embed | Turn each complaint into a 384-dim meaning-vector | `sentence-transformers` (MiniLM) |
| 3️⃣ Cluster | Group similar complaints into themes | `scikit-learn` (KMeans) |
| 4️⃣ Severity | Score negativity + high-stakes terms | `VADER` |
| 5️⃣ Prioritize | Rank by **volume × severity** | — |
| 6️⃣ Name | Give each theme a clear human label | `Google Gemini` (LLM) |
| 7️⃣ Deliver | Interactive dashboard + upload analyzer | `Streamlit`, `Plotly` |

---

## 📊 Key results — 112,481 credit-card complaints (2023–2026)

- 🥇 **#1 problem: Unauthorized / fraudulent charges** — the most common *and* most severe (13.4% of all complaints).
- Followed by merchant/refund disputes, inaccurate credit-reporting, payment-processing errors,
  unauthorized applications, and identity theft.
- Running on the full 112k (vs an 18k sample) produced **cleaner, more distinct themes** — a real,
  documented finding.

<p align="center"><i>Priority matrix & theme charts live in <code>project1_insight_engine/outputs/</code> and render interactively in both dashboards.</i></p>

---

## 📓 Notebooks (read the story top-to-bottom)

| Notebook | What it covers |
|----------|----------------|
| [`phase1_data.ipynb`](project1_insight_engine/notebooks/phase1_data.ipynb) | Getting & profiling the raw CFPB data (incl. a real data-corruption bug we caught) |
| [`phase2_clean.ipynb`](project1_insight_engine/notebooks/phase2_clean.ipynb) | Cleaning the complaint text without destroying meaning |
| [`phase3_engine.ipynb`](project1_insight_engine/notebooks/phase3_engine.ipynb) | The NLP engine, prototyped on an 18k sample |
| [`phase3_full_depth.ipynb`](project1_insight_engine/notebooks/phase3_full_depth.ipynb) | **The full-depth run on all 112k complaints** — theory, reproducibility check, business insights, honest limitations |

Every code cell has a header, inline comments, an explanation before it runs, and an interpretation
of its output. Colorful markdown, emojis, and runnable outputs throughout.

---

## 🖥️ Run it locally

```bash
python -m venv .venv
.venv\Scripts\activate                                   # Windows
pip install -r project1_insight_engine/requirements.txt
streamlit run project1_insight_engine/app/insight_app.py
```

---

## 🛠️ Tech stack
`Python` · `pandas` · `Parquet` · `sentence-transformers (all-MiniLM-L6-v2)` · `scikit-learn (KMeans, TF-IDF, PCA)` ·
`VADER` · `Google Gemini (LLM)` · `Streamlit` · `Plotly` · `Git / GitHub`

---

## 🗺️ Roadmap
- [x] Data profiling & validation (17M-row source, chunked)
- [x] Text cleaning (112k clean complaints)
- [x] NLP engine — embeddings → clustering → severity → priority → LLM naming
- [x] Full-depth analysis notebook (real 112k run)
- [x] Interactive Streamlit dashboard + upload-and-analyze mode
- [x] **Live public deployment** (Streamlit Community Cloud + GitHub Pages)
- [ ] Scheduled auto-refresh (GitHub Actions)

---
<p align="center"><i>Data science portfolio project by <b>Swagata Bhowmik</b> · built on real public data, defensible end-to-end.</i></p>
