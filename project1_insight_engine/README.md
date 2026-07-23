# 🔍 Insight Engine — Mining Customer Complaints for the Top Problems to Fix

> **One line:** Turn a huge pile of raw customer-complaint text into a ranked, actionable list
> of the top recurring problems — delivered as an interactive dashboard and an upload platform
> anyone can use.

---

## The business problem
Companies receive thousands of customer complaints in plain English. Nobody can read them all,
so the most valuable signal — *"what is actually going wrong and what should we fix first?"* —
stays buried. This project mines that text automatically and turns it into decisions.

## What it does
1. **Ingests & cleans** raw complaint text.
2. **Groups** similar complaints into recurring *themes* using NLP (embeddings + clustering).
3. **Names** each theme in plain English using an LLM.
4. **Ranks** themes by frequency × severity → a "fix these first" list.
5. **Delivers** results via an interactive dashboard + an upload platform (drop a file, get answers).
6. **Automates** a weekly refresh of "top new issues" (optional, hands-off).

## Data
**CFPB Consumer Complaint Database** — U.S. government open data (~7.8M real complaints,
1M+ with written narratives). Public, free, legally clean. Source:
https://www.consumerfinance.gov/data-research/consumer-complaints/

> Chosen over app-store scraping (legal/ToS risk, small, unreliable) and generic review datasets
> (overdone, not problem-focused). The same pipeline works on any company's complaint/review data.

## Tech stack
Python · pandas · sentence-transformers · scikit-learn / HDBSCAN · an LLM (Gemini/Groq free tier)
· Streamlit (platform) · GitHub Actions (free automation).

## Project phases
- **Phase 1 — Data:** get the data, understand it, first look. ⬜
- **Phase 2 — Clean:** clean & prepare the complaint text. ⬜
- **Phase 3 — Engine:** embed → cluster → name → rank (the core NLP). ⬜
- **Phase 4 — Platform:** the Streamlit upload app + dashboard. ⬜
- **Phase 5 — Automation:** scheduled auto-refresh (optional). ⬜

## Status
🚧 In progress — Phase 1.

---
*Part of Swagata Bhowmik's data science portfolio. Built on real public data, defensible end-to-end.*
