# 🎯 MASTER PLAN — Resume + Portfolio Projects (Swagata Bhowmik)

> **Purpose of this file:** a complete, self-contained handoff. It holds (1) the finalized
> resume plan, (2) the 4 portfolio projects in depth, (3) the exact public data to download,
> (4) the software/tools to install, and (5) how each project maps back to the resume.
> Built so it can be carried into a fresh chat/folder and worked on step by step.
> **Golden rule everywhere:** nothing goes on the resume until it is actually built and
> can be defended line-by-line. No fabrication. Real public data only.

---

# PART 0 — WHO THIS IS FOR & TARGET ROLES

- **Candidate:** Swagata Bhowmik — MSc Data Science, NMIMS Mumbai (2025–present, CGPA 9.14).
- **Targeting:** Data Analyst · Data Scientist · Data Engineer · AI Engineer · Agentic AI.
- **Big existing credentials:** HDFC Bank internship (Digital Banking) + Colgate DATAVERSE
  Hackathon 1st Runner-Up. These go in **Experience** and **Honors**, NOT in Projects.
- **Theme to sell across everything:** clean data first → honest, defensible results →
  turned into a decision → and where possible, **automated so it runs itself**.

### ⚙️ COMPUTE — CONFIRMED (2026-07-22)
- **Machine:** DESKTOP-V0671UV — Windows 11 Home (25H2, x64)
- **CPU:** Intel Core i7-8650U @ 1.90GHz (older mobile chip; fine for analysis, weak for GPU-heavy work)
- **RAM:** 32 GB (excellent — comfortable for data cleaning, CPU embeddings, moderate datasets)
- **GPU:** NVIDIA GeForce MX150 (2 GB) — **treated as "no usable GPU"** (too small for local LLMs / fine-tuning) + Intel UHD 620 (integrated)
- **Storage:** ~640 GB free (plenty)
- **Effective setup:** **Laptop (local) + free cloud GPU (Colab/Kaggle T4)** for heavy parts.

**What this means per project:**
- **P1 (Insight Engine):** fully local. Embeddings on CPU are fine for moderate volumes.
- **P2 (Persuadables):** fully local.
- **P3 (Grounded RAG):** local dev; embeddings on CPU OK; use hosted LLM API for generation; run any heavy re-ranking/eval batches on Colab if slow.
- **P4 (Extractor / fine-tuning):** **must use free Colab/Kaggle T4** for QLoRA. Cannot fine-tune locally.

### 🤖 LLM PROVIDER — CONFIRMED (free-first, 2026-07-22)
- **Primary:** Google Gemini free tier (strong quality, generous limits).
- **Backup:** Groq free tier (very fast).
- **Offline fallback:** Ollama local (small models only — CPU is slow, use sparingly).
- Code will be written so switching providers is a one-line change. No paid key unless chosen later.

### 🗂️ DOCUMENT VERSIONING — CONFIRMED (2026-07-22)
- `Resume Plan.md` (this file, at workspace root) = the **living source of truth**, always current.
- Before each major upgrade, a numbered frozen snapshot is saved into `/versions/`
  (e.g. `Resume Plan v01 (original).md`, `v02`, ...). Snapshots are never edited.
- A running **DECISIONS LOG** is kept at the bottom of this file.

---

# PART 0.5 — HOW WE WORK TOGETHER (PERMANENT RULES — never skip these)

> These rules apply to EVERY session and EVERY project from now on. They are non-negotiable.
> They exist because the real goal is not just "build projects" — it is to make Swagata
> **placement-ready**: able to explain, defend, and be questioned on everything we build.

### Rule 1 — Teach like she's a complete beginner
- Assume zero prior knowledge of the tools, libraries, or theory.
- Explain every new term in plain language the first time it appears. No unexplained jargon.
- Explain WHAT we're doing, WHY we're doing it, and the THEORETICAL meaning behind it.

### Rule 2 — Ask before doing anything
- Never start building, installing, or downloading without saying what it is and getting a "yes".
- Always give physical, step-by-step guidance: where to go, what to open, what to click,
  where to paste the code. Nothing assumed.

### Rule 3 — This is placement prep, not just building
For every project, Swagata must end up able to answer:
- What did I build, and what business problem does it solve?
- How did I build it (each step, each tool, each model choice)?
- What is the theory behind it / what does it mean?
- How could an interviewer question me on this? (We collect likely interview Q&A as we go.)
- What mistakes did we make, and what did I learn from them? (We log mistakes honestly.)

### Rule 4 — Realistic and honest only (Kiro is the cross-checker)
- There is NO other supervisor. Kiro must sanity-check every result before showing it:
  is this logical? is this realistic? does this make business sense?
- No inflated, cherry-picked, or "too good to be true" results. If a result looks wrong,
  we investigate it, we don't hide it.
- We always view the problem from a BUSINESS perspective, then build.

### Rule 5 — Code discipline (EVERY cell, EVERY time — no reminders needed)
Every piece of code given must have ALL of the following:
1. **Header** — a top comment saying what this cell is about.
2. **Inline comments** — explaining how the code works as it goes.
3. **Interpretation (before running)** — what this code does and what it will give us.
4. **Interpretation of output (after running)** — what the result actually means. Output
   without interpretation is worthless.

### Rule 6 — One cell at a time (strict)
- Give code ONE cell at a time, never a big dump.
- Swagata pastes it, runs it. If there's an error, she shares it, Kiro fixes it right there.
- Only after a cell works do we move to the next cell.

### Rule 7 — Maintain the notebook & bring the right tools
- We maintain a working notebook (e.g. Jupyter / VS Code notebook) per project.
- Kiro may introduce any additional tools/libraries that make the work better — but must
  always explain what the tool is and why we're using it.

### Rule 8 — Maintain the Learning Journal (`Learning Journal.md`)
- A separate file `Learning Journal.md` is Swagata's personal placement study guide.
- Every time we do something new, Kiro APPENDS an entry with: What we did · Why · What it
  means (theory, plain language) · Interpretation · Interview angle (likely Q + strong short
  answer) · Mistakes/gotchas.
- Append-only, newest at the bottom, with a table of contents kept updated.
- This is how theory + interview prep is captured continuously, not left to the end.

---

# PART 1 — FINALIZED RESUME PLAN

> Layout/design done later. This is the CONTENT and STRUCTURE only.
> Full confirmed content also lives in `CV_Content.md`.

## Structure (sections in order)
1. **Header** — Name · Mumbai · 6375543596 · okswagata@gmail.com · linkedin.com/in/swagata-bhowmik · github.com/Swagata-Bhowmik
2. **Professional Summary** — neutral (works for jobs + campus placement)
3. **Education** — MSc (NMIMS, CGPA 9.14) · B.Sc. CS/Math/Stats (St Joseph's, Bangalore, 2020–2023) · Class 12 (KV No.6 Jaipur, 2019–2020) · Class 10
4. **Experience** — HDFC (Project Trainee) + Dotsquares + SynthWave + Xedi
5. **Projects** — the 3–4 NEW self-built projects (this file's focus)
6. **Skills** — Python, R, SQL, Excel, Power BI, Tableau, PySpark, Databricks, scikit-learn, + ML/DL/NLP/GenAI
7. **Honors & Awards** — Colgate DATAVERSE Hackathon (1st Runner-Up)
8. **Certifications** — Data Analytics with Python (NPTEL), Cloud Computing (NPTEL)
9. **Extra-curricular** — Badminton; regional Kho-Kho & Chess; Videography/Editing; Ukulele

## What already covers which "in-demand pillar"
- **Customer Segmentation & Retention** → covered by **HDFC** (Experience).
- **Demand Forecasting / Time-Series** → covered by **Colgate** (Honors).
- So the Projects section fills the REMAINING pillars: **NLP, Experimentation/Uplift,
  Deployment, Production RAG, Agentic AI, Fine-tuning, Automation.**

## HDFC — Experience bullets (truthful, defendable — already real work)
- Built a trusted single-customer view over data at the scale of crores of records;
  focused on understanding, cleaning, reconciling and validating data before modelling.
- Created customer-ID resolution logic; turned it into a reusable tool returning the correct
  customer from any identifier, with a confidence label per match.
- Built an ML adoption model to rank customers likely to start Net Banking (validated with
  lift & KS); delivered a ranked, reason-tagged target list.
- Benchmarked HDFC vs peers on digital-payment metrics using authentic public sources;
  turned a 118-response survey into an interactive dashboard.
- Tools: Python, SQL, PySpark, Azure Databricks, scikit-learn, Power BI.

## Colgate — Honors entry (truthful)
- 1st Runner-Up, DATAVERSE Hackathon 2026 (Colgate Global Business Services × NMIMS NSoMASA),
  Team Vector³. Designed a data-driven launch strategy for a new bundle with zero historical
  sales: engineered latent demand from basket behaviour, built a multi-model 12-week forecast
  (Prophet, Regression, Random Forest, Ensemble), ran price optimization to maximize total
  category margin, delivered via a Power BI dashboard.

---

# PART 2 — THE PORTFOLIO (Option B: 4 projects, automation woven in)

> Build ONE at a time. Only add to resume once built + defendable.
> Each project = business problem → real data → build → evaluation → artifact (dashboard/app)
> → automation angle → CV bullet.

## 🗺️ Portfolio overview

| # | Project (working name) | Roles it targets | Automation angle | Priority |
|---|------------------------|------------------|------------------|----------|
| 1 | **Insight Engine** — NLP themes + BI dashboard | Analyst, Scientist, (GenAI) | auto-ingest + weekly auto-report | build 1st |
| 2 | **Persuadables** — Uplift + Experimentation + Deployment | Scientist, MLOps/Data Eng | self-updating / auto-retrain | build 3rd |
| 3 | **Grounded** — Agentic RAG + Monitoring (FLAGSHIP) | AI Engineer, Agentic AI, Data Eng | agent that acts + auto-eval in CI | build 2nd |
| 4 | **Extractor** — Fine-tuning (LoRA + DPO) | AI Engineer | automated before/after eval | build 4th (needs GPU) |

> Optional 5th showpiece (only if time): **Agentic Analyst** — plain-English question →
> agent writes SQL → runs on real DB → chart + summary (pure automation of an analyst's job).

---

## 📦 PROJECT 1 — "Insight Engine"
**NLP insights from unstructured text + a BI dashboard (+ automation)**

### The business problem
Companies drown in text — reviews, complaints, tickets — and never mine it. Turn a huge pile
of raw customer text into the **top fixable problems, ranked by frequency × negativity**, so a
product/ops team knows what to fix first.

### Why it's good for you
- Hits **Data Analyst** (dashboard/BI), **Data Scientist** (NLP/clustering), and a touch of
  **GenAI** (LLM summarizes each theme). One project, three role-signals.
- Not "sentiment analysis" (dead) — real insight extraction.

### Real public data (to download — VERIFY LINK LOADS before committing)
- **Primary option:** US Consumer Financial Protection Bureau (CFPB) Complaints — millions of
  real complaints, public, banking-flavoured (ties to HDFC). Search: "CFPB consumer complaint
  database download".
- **Alt option:** Amazon Product Reviews (Kaggle: "amazon product reviews") or Yelp Open Dataset
  (yelp.com/dataset).
- *(We will scrape/verify the exact working link in the build chat.)*

### Build plan (phases)
1. **Ingest + clean** the text (handle nulls, dedupe, normalize).
2. **Embed** each document with **Sentence Transformers** (e.g. all-MiniLM-L6-v2).
3. **Cluster** embeddings (K-Means or HDBSCAN) to find recurring themes.
4. **Summarize/label** each cluster with an LLM (name the theme, 1-line description).
5. **Rank** themes by volume × negativity → "top problems to fix."
6. **Dashboard** in Power BI or Streamlit — filter by product/time, drill into a theme.
7. **Automation:** schedule ingestion of new text → re-cluster → auto-generate a
   "top 5 new issues this week" report (email/Slack or a refreshed dashboard page).

### Tools/libraries
Python, pandas, sentence-transformers, scikit-learn (KMeans) or hdbscan, umap-learn (viz),
an LLM (OpenAI API or a local Ollama model), Power BI Desktop OR Streamlit.

### Evaluation (how you defend it)
- Cluster quality: silhouette score + human check ("are these themes meaningful?").
- Usefulness: can someone act on the top-5 list? Show an example.

### CV bullet (draft — finalize after building)
- "Built an NLP insight engine over [N] real customer complaints: embedded and clustered text
  to surface the top recurring issues ranked by frequency and severity, delivered via an
  interactive dashboard with an automated weekly refresh."

---

## 📦 PROJECT 3 — "Grounded" (FLAGSHIP — build 2nd)
**Production-grade Agentic RAG with citations + monitoring (+ automation)**

### The business problem
Let a user ask questions over a real document set and get **trustworthy, cited answers** — and
make it an **agent** that decides when to retrieve, when to use a tool, and refuses to answer
when it lacks evidence. This is the #1 enterprise AI pattern + agentic + automation in one.

### Why it's good for you
- Directly targets **AI Engineer + Agentic AI + Data Engineer**.
- Matches your Sem-3 syllabus (GenAI, NLP, MLOps) and your earlier RAG interest.

### Real data / corpus (public)
- A real document corpus you choose: e.g. Indian govt scheme PDFs / RBI circulars / a set of
  research papers / drug leaflets (openFDA). Public and downloadable.
- *(Exact corpus + links finalized in build chat.)*

### Build plan (3 phases)
**Phase 1 — fundamentals:** ingest PDFs/markdown/web → chunk 500–800 tokens, ~100 overlap →
embed → store in **ChromaDB** → retrieve top-k → answer **with citations to the exact paragraph**.
**Phase 2 — production quality:** **hybrid retrieval** (BM25 + vector) → **cross-encoder
re-ranker** → **citation enforcement** (decline if evidence insufficient) → prompts in a
versioned config file.
**Phase 3 — agentic + shippable:**
- **Agent layer** (LangGraph): the agent decides retrieve vs tool-call vs answer; can chain
  steps (read → decide → act → verify → cite).
- **Golden eval set** (50–200 verified Q&A) → offline **faithfulness** eval (RAGAS).
- **Monitoring** (Langfuse): trace every step; track latency P50/P95, cost/request, citation
  coverage, failure rate; dashboard.
- **Automation / CI:** eval runs automatically; build fails if faithfulness drops.

### Tools/libraries
LangChain / **LangGraph**, **ChromaDB**, sentence-transformers (embeddings + cross-encoder),
rank-bm25, **RAGAS**, **Langfuse** (self-host), an LLM (OpenAI API or **Ollama** local),
Streamlit (UI), optionally FastAPI.

### Evaluation (defend it)
- Faithfulness / answer-relevance (RAGAS), citation coverage %, before/after re-ranker precision.

### CV bullet (draft)
- "Built a production-grade agentic RAG assistant with hybrid retrieval, cross-encoder
  re-ranking and citation enforcement; added monitoring (latency, cost, faithfulness) and an
  automated evaluation gate in CI."

---

## 📦 PROJECT 2 — "Persuadables" (build 3rd)
**Experimentation + Uplift modeling + deployment (+ automation)**

### The business problem
Don't just predict who converts — find **who converts BECAUSE of the campaign** (persuadables),
so marketing spend goes only where it changes behaviour. Rare in portfolios = big differentiator.
Extends your HDFC targeting story.

### Real public data
- **Criteo Uplift** dataset (real, large, public) OR a Kaggle A/B testing dataset.
- *(Exact link verified in build chat.)*

### Build plan
1. **A/B analysis:** define metric, check assumptions, statistical vs practical significance.
2. **Uplift model:** two-model / uplift-tree / meta-learners → segment into persuadables,
   sure-things, lost-causes, sleeping-dogs.
3. **Power analysis:** was the sample big enough?
4. **Segment results** (new vs loyal, device, etc.).
5. **Decision:** who to target, ship/no-ship, roll-out plan.
6. **Deploy:** Streamlit app — input a customer → uplift score + recommended action.
7. **Automation:** pipeline auto-retrains on new data + auto-refreshes the target list.

### Tools/libraries
Python, pandas, scikit-learn, **causalml** or **scikit-uplift**, statsmodels/scipy (stats),
Streamlit, MLflow (experiment tracking).

### CV bullet (draft)
- "Built an uplift-modeling pipeline that identifies persuadable customers from A/B data,
  deployed as a self-updating Streamlit app with auto-retraining."

---

## 📦 PROJECT 4 — "Extractor" (build 4th — needs GPU)
**Fine-tuning a small LLM for structured extraction (LoRA + DPO)**

### The business problem
Turn messy unstructured text into **clean structured JSON** (e.g. extract fields from invoices,
contracts, or medical notes) — a real, common enterprise need where prompting alone falls short.
Prove a measurable **before vs after**.

### Real public data
- A clean instruction/extraction dataset (2k–10k examples) from Hugging Face; or build a small
  clean set from a public documents corpus.
- *(Exact dataset finalized in build chat.)*

### Build plan
1. **Baseline:** best result with careful prompting only (measure JSON validity, accuracy).
2. **SFT with LoRA/QLoRA** on a clean dataset; base model e.g. Qwen-2.5/3 ~7-8B; on Colab/Kaggle T4.
3. **Eval:** JSON validity rate, exact-match accuracy, refusal correctness.
4. **DPO preference tuning:** good vs worse outputs → improvement over SFT.
5. **Report:** training curve, before/after table, honest "what went wrong & how I fixed it."
6. **Automation:** an automated eval script that runs the test set and prints the metrics.

### Tools/libraries
Hugging Face **transformers + TRL + PEFT (LoRA/QLoRA)**, datasets, bitsandbytes, Colab/Kaggle GPU,
optionally Axolotl.

### CV bullet (draft)
- "Fine-tuned a small LLM (LoRA + DPO) for structured JSON extraction, improving JSON-validity
  from X% (prompt-only) to Y%, with an automated evaluation pipeline."

---

# PART 3 — SOFTWARE / TOOLS TO INSTALL (one-time setup for the new folder)

### Core (all projects)
- **Python 3.11+** (Anaconda or plain Python)
- **VS Code** (editor) + Python extension
- **Git** + a **GitHub** account (push every project — recruiters check GitHub)
- **Jupyter** (comes with Anaconda) or use VS Code notebooks

### Python packages (install per project via pip/conda — a requirements.txt per project)
- General: `pandas numpy matplotlib seaborn scikit-learn jupyter`
- NLP/embeddings: `sentence-transformers hdbscan umap-learn`
- RAG/agentic: `langchain langgraph chromadb rank-bm25 ragas langfuse`
- Uplift: `causalml` or `scikit-uplift`, `statsmodels scipy`
- Fine-tuning: `transformers trl peft datasets bitsandbytes accelerate`
- Apps/deploy: `streamlit fastapi uvicorn`
- Tracking: `mlflow`

### Apps / accounts
- **Power BI Desktop** (free, Windows) — for BI dashboards (Project 1).
- **Ollama** (ollama.com) — run local LLMs (Projects 1/3, optional).
- **Google Colab** or **Kaggle** account — free GPU (Projects 3/4).
- **OpenAI (or other) API key** — optional, if not using local LLMs.
- **Langfuse** (self-host via Docker) — monitoring (Project 3). Needs **Docker Desktop**.

### Suggested folder layout (in the new folder)
```
portfolio/
  project1_insight_engine/
    data/  notebooks/  app/  README.md  requirements.txt
  project2_persuadables/
    data/  notebooks/  app/  README.md  requirements.txt
  project3_grounded_rag/
    data/  src/  eval/  app/  README.md  requirements.txt
  project4_extractor/
    data/  notebooks/  README.md  requirements.txt
  MASTER_PLAN_Resume_and_Projects.md   <-- this file
  CV_Content.md
```

---

# PART 4 — DATA TO DOWNLOAD (checklist — verify each link works first)

| Project | Dataset | Where to get it | Status |
|---------|---------|-----------------|--------|
| 1 | CFPB Consumer Complaints (or Amazon Reviews / Yelp) | CFPB open data portal / Kaggle / yelp.com/dataset | ⬜ verify + download |
| 2 | Criteo Uplift (or Kaggle A/B dataset) | Criteo AI Lab / Kaggle | ⬜ verify + download |
| 3 | Document corpus (govt PDFs / papers / openFDA labels) | official public sources | ⬜ choose + download |
| 4 | Clean extraction/instruction dataset (2k–10k) | Hugging Face datasets | ⬜ choose + download |

> ⚠️ In the build chat we will confirm each dataset actually exists, is public, downloadable,
> and big/clean enough — BEFORE committing to it. No synthetic data unless explicitly agreed.

---

# PART 5 — BUILD ORDER & DEFINITION OF DONE

**Build order:** P1 (Insight Engine) → P3 (Grounded RAG flagship) → P2 (Persuadables) → P4 (Extractor).

**A project is "DONE" (resume-ready) only when:**
- [ ] It runs end-to-end on real data.
- [ ] There's a visible artifact (dashboard/app) + a clean GitHub repo with README.
- [ ] You understand and can defend every step, model choice, and metric.
- [ ] It has an evaluation section (real numbers) and an automation angle.
- [ ] The CV bullet is written from what actually happened (no inflation).

**Final step (after projects built):** drop the finalized project bullets into the resume
Projects section, keep HDFC in Experience and Colgate in Honors, then finalize layout + export
to PDF/Word.

---

# PART 6 — QUICK CONTEXT FOR A NEW CHAT (paste-friendly summary)
"I'm Swagata, MSc Data Science (NMIMS). Targeting Data Analyst/Scientist/Engineer + AI/Agentic
roles. I have real HDFC internship experience (data cleaning/identity resolution/targeting model/
benchmarking/survey) and a Colgate hackathon win (bundle demand forecast + price optimization).
I'm building 4 portfolio projects on REAL public data, one at a time, and I must be able to
defend every line (no fabrication). The 4: (1) NLP Insight Engine + BI dashboard, (2) Uplift/
Experimentation + deployment, (3) Agentic RAG + monitoring [flagship], (4) LLM fine-tuning for
JSON extraction. Automation is woven into each. See this MASTER_PLAN file for full details.
My compute is: [FILL IN]. Let's build Project [X] — start by confirming the real dataset."
```
```


---

# PART 7 — DECISIONS LOG (append-only; newest at bottom)

### 2026-07-22 — Session 1: Kickoff & ground-truths established
- Read and understood the full master plan. Confirmed goal: build 3–4 real, defensible
  portfolio projects on real public data, one at a time, then finalize the resume.
- **Compute confirmed:** i7-8650U / 32GB RAM / MX150 2GB (no usable GPU) / Windows 11.
  Decision → local for P1 & P2; free Colab/Kaggle T4 for the heavy parts of P3 & P4.
- **LLM provider confirmed:** free-first — Gemini (primary) → Groq (backup) → Ollama (offline
  fallback). Provider-swappable code.
- **Versioning confirmed:** living `Resume Plan.md` + numbered frozen snapshots in `/versions/`.
  Saved `versions/Resume Plan v01 (original).md`.
- Golden rules reaffirmed: nothing on the resume until built + defendable; real public data only;
  no fabrication; no synthetic data unless explicitly agreed.
- **Next step:** begin Project 1 (Insight Engine) — start by verifying/confirming the real
  dataset (CFPB Consumer Complaints as primary candidate) before any building.

### 2026-07-22 — Session 1 (cont.): Working-style rules locked
- Added PART 0.5 "HOW WE WORK TOGETHER" as permanent rules:
  (1) teach like a complete beginner, (2) ask before doing anything + always give
  step-by-step physical guidance, (3) placement prep — theory + interview Q&A + mistakes log
  for every project, (4) realistic/honest only, Kiro is the cross-checker (no other supervisor),
  (5) code discipline: header + comments + interpretation of code + interpretation of output
  on every cell, (6) one cell at a time with error-fix loop before moving on, (7) maintain a
  notebook and explain any new tool introduced.
- These rules apply to all future sessions and projects.

### 2026-07-22 — Session 1 (cont.): Learning Journal created
- Checked machine: Python 3.14 + 3.13 (two versions), Jupyter, pip, Git, VS Code, pandas,
  numpy, scikit-learn all already installed. No Anaconda needed.
- Flagged two issues: (1) two Pythons out of sync (Jupyter on 3.13 lacks the libs), (2) 3.14
  too new for some AI libs. Decision → create one isolated virtual env on stable Python 3.13.
- Added Rule 8 + created `Learning Journal.md` (append-only interview/theory study guide).
  Seeded it with Entry 001 (dev tools) and Entry 002 (virtual environments).
- Next step: create & activate the project virtual environment (Python 3.13), then start P1.
- **Working environment decided:** VS Code as the editor, Jupyter notebooks (.ipynb) opened
  INSIDE VS Code (not classic browser Jupyter). Same cell-by-cell style. Note for beginner:
  Jupyter is the notebook *format*; VS Code is the *editor* it runs inside — they work together.
