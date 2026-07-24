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
</p>

---

## 💡 Overview
Companies receive thousands of customer complaints in plain English — far too many to read. This
project uses NLP to automatically discover the **recurring problems** hidden in that text and ranks
them by **how common and how severe** they are, so a team knows exactly what to fix first.

Built **end-to-end on real public data** (US CFPB Consumer Complaint Database). No fabrication —
every result traces back to real complaints and can be defended step by step.

## 🧠 How it works
| Step | What happens | Tools |
|------|--------------|-------|
| 1. Ingest & clean | De-duplicate, normalize privacy masks, keep meaning | `pandas`, `regex`, `Parquet` |
| 2. Embed | Turn each complaint into a 384-dim meaning-vector | `sentence-transformers` (MiniLM) |
| 3. Cluster | Group similar complaints into themes | `scikit-learn` (KMeans) |
| 4. Severity | Score negativity + high-stakes terms | `VADER` |
| 5. Prioritize | Rank by **volume × severity** | — |
| 6. Name | Give each theme a clear human label | `Google Gemini` (LLM) |
| 7. Deliver | Interactive dashboard + upload analyzer | `Streamlit`, `Plotly` |

## 📊 Key results — 112,481 credit-card complaints (2023–2026)
- **#1 problem: Unauthorized / fraudulent charges** — the most common *and* most severe.
- Followed by merchant/refund disputes, credit-reporting issues, payment-processing errors,
  unauthorized applications, and identity theft.
- Running on the full 112k (vs a sample) produced cleaner, more distinct themes.

<p align="center"><i>Priority matrix & theme charts are in <code>project1_insight_engine/outputs/</code>.</i></p>

## 🖥️ The app
An interactive Streamlit dashboard that tells the whole story (Problem → Data → Cleaning → Engine →
Results), **plus an upload mode** where anyone can drop in their own complaints file and get an
instant ranked breakdown.

```bash
python -m venv .venv
.venv\Scripts\activate                                   # Windows
pip install -r project1_insight_engine/requirements.txt
streamlit run project1_insight_engine/app/insight_app.py
```

## 🗂️ Project structure
```
project1_insight_engine/
├── notebooks/     # data profiling, cleaning, and the NLP engine (phase 1–3)
├── app/           # insight_app.py — the interactive Streamlit dashboard
├── outputs/       # generated charts (priority matrix, theme sizes, meaning-map)
├── README.md      # detailed write-up
└── requirements.txt
```
> The 8.5 GB raw dataset and generated embeddings are not committed (large / re-downloadable).

## 🗺️ Roadmap
- [x] Data profiling & validation (17M-row source, chunked)
- [x] Text cleaning (112k clean complaints)
- [x] NLP engine — embeddings → clustering → severity → priority → LLM naming
- [x] Interactive Streamlit dashboard
- [ ] Public deployment (Streamlit Community Cloud)
- [ ] Scheduled auto-refresh (GitHub Actions)

---
<p align="center"><i>Data science portfolio project by <b>Swagata Bhowmik</b>.</i></p>
