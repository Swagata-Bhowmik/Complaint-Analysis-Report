# 📚 LEARNING JOURNAL — Theory, Meaning & Interview Prep (Swagata Bhowmik)

> **Purpose:** This is Swagata's personal study guide for placements. Every time we do
> something new, Kiro appends an entry here explaining — in plain language — WHAT we did,
> WHY we did it, WHAT it means, and HOW to talk about it in an interview.
> Read this before any interview. It is append-only (newest entries at the bottom).

> **How to read each entry:**
> - **What we did** — the action, in one line.
> - **Why we did it** — the reason / business or technical motivation.
> - **What it means (theory)** — the concept explained simply.
> - **Interpretation** — how to read the result/output.
> - **Interview angle** — likely questions + a strong short answer ("soundbite").
> - **Mistakes / gotchas** — what can go wrong and what we learned.

---

## 📖 TABLE OF CONTENTS
- Entry 001 — Development setup: Python, Jupyter, pip, Git (what each tool is)
- Entry 002 — Virtual environments (isolated project "rooms")
- Entry 003 — Choosing the dataset: why CFPB, and why not scraping (data sourcing & compliance)
- Entry 004 — Project 1 vision + automation levels (on-demand, scheduled, alerting)

---

## Entry 001 — Development setup: the tools on our machine
**Date:** 2026-07-22 · **Context:** Project 1 setup (checking the computer before building)

**What we did:** Checked what was already installed on the computer instead of blindly installing.

**Why we did it:** Installing things you already have creates clutter and conflicts. A pro
always checks the environment first.

**What it means (theory) — the tools, in plain words:**
- **Python** — the programming language we write our data code in.
- **Jupyter Notebook** — a workspace where code is written and run in small blocks called
  "cells", with notes and results shown right below each cell. Great for learning and for
  showing your thinking step-by-step.
- **pip** — Python's package installer (like an app store for Python tools/"libraries").
- **library / package** — a pre-built bundle of code someone else wrote that we reuse
  (e.g. `pandas` for tables, `scikit-learn` for machine learning).
- **Git** — a tool that tracks changes to your code and lets you upload projects to GitHub
  (recruiters check GitHub).
- **VS Code** — a code editor; a nicer place to write and manage project files.

**Interpretation:** We found Python, Jupyter, pip, Git, VS Code, pandas, numpy, and
scikit-learn already installed — so we did NOT need Anaconda.

**Interview angle:**
- Q: "How do you set up a data science project?"
  A: "I check what's already installed, then create an isolated environment per project so
  dependencies are reproducible and don't conflict."

**Mistakes / gotchas we hit:**
- The machine had **two Python versions** (3.14 and 3.13) installed at once, and Jupyter was
  tied to the one WITHOUT our libraries. Lesson: multiple Pythons cause "I installed it but
  it says not found" errors. The fix is an isolated environment (Entry 002).
- Python 3.14 was very new; heavy AI libraries often lag behind the newest Python, so we
  chose the more stable 3.13 as our base. Lesson: newest ≠ safest for real projects.

---

## Entry 002 — Virtual environments (isolated project "rooms")
**Date:** 2026-07-22 · **Context:** Project 1 setup

**What we did:** Decided to create one clean, isolated virtual environment for the project
based on the stable Python 3.13.

**Why we did it:** To avoid the two-Python conflict and keep every project's tools separate.

**What it means (theory):** A virtual environment is a private, self-contained copy of Python
+ its installed libraries, living in one folder. Analogy: your computer is a house; instead of
dumping all tools in one shared room where projects fight over versions, each project gets its
own private room with its own tools. Delete the room = clean slate, rest of the computer
untouched.

**Interpretation:** Once activated, anything we `pip install` goes only into that environment,
and the notebook runs against exactly those tools — no surprises.

**Interview angle:**
- Q: "Why use virtual environments?"
  A: "So dependencies never conflict across projects and the setup is reproducible — anyone can
  recreate my environment from a requirements file and get the same result."
- Term to know: **reproducibility** — someone else can rebuild your exact setup and get the
  same results.

**Mistakes / gotchas:** Forgetting to *activate* the environment before installing/running is
the classic beginner mistake — you then install into the wrong place. Always confirm the
environment name shows in the terminal prompt before working.

---

## Entry 003 — Choosing the dataset: why CFPB (data sourcing & compliance)
**Date:** 2026-07-22 · **Context:** Project 1, deciding the data

**What we did:** Compared public datasets and chose the **CFPB Consumer Complaint Database**.

**Why we did it:** The data is the foundation of the whole project, so it must be real, free,
large, legally clean, and about actual *problems* (not just star ratings).

**What it means (theory) — how to judge a dataset:**
- **Authentic** — real people, not synthetic/AI-generated (fake data can't be defended).
- **Legal / compliant** — we're allowed to use it. Government open data = yes.
- **Fit for purpose** — has the fields we need (here: the written *narrative* = the problem text).
- **Size** — big enough to find real patterns (~7.8M complaints, 1M+ with narratives).
- **Story** — ties to Swagata's HDFC banking background = one coherent resume narrative.

**Why NOT the alternatives (important interview point):**
- **Play Store / App Store scraping** — visible publicly but scraping violates Terms of Service,
  is technically brittle (blocks, rate limits, only ~40–200 reviews), and involves personal data
  (privacy law). "Publicly visible" ≠ "free & safe to bulk-collect."
- **Amazon/Yelp/IMDB** — legal but generic/overdone, and IMDB is sentiment-only ("dead" per plan).
- **Synthetic HuggingFace sets** — fake data, breaks the "real data only" rule.

**Interview angle:**
- Q: "Why did you choose this dataset?"
  A: "I chose an authoritative open-data source (CFPB) because it's legally clean, large, and
  contains real complaint narratives. I deliberately avoided scraping app-store reviews because
  that violates platform terms, is unreliable, and raises privacy issues. Data sourcing and
  compliance matter as much as the modelling."
- Term: **compliance** — following the legal/contractual rules about what data you may use.

**Mistakes / gotchas:** Not every CFPB complaint has a narrative (it's opt-in). We must filter to
rows WHERE narrative is present — still leaves 1M+ real text complaints.

---

## Entry 004 — Project 1 vision + automation (is it possible? is it free?)
**Date:** 2026-07-22 · **Context:** Project 1, scope & automation

**What we did:** Defined the full vision and the automation levels.

**The vision (what to say about the project):** "I built a system that reads thousands of raw
customer complaints and automatically surfaces the top recurring problems, ranked by frequency and
severity, so a manager can see what to fix first — delivered as a dashboard and an upload platform
where anyone can drop in a complaints file and get answers back."

**Automation — three levels, all FREE:**
- **Level 1 — On-demand upload platform:** a Streamlit web app; user uploads CSV/Excel → gets
  ranked problems + downloadable report. Hosted free on Streamlit Community Cloud. (Headline deliverable.)
- **Level 2 — Scheduled auto-refresh:** GitHub Actions (free) runs the pipeline on a timer
  (e.g. weekly), pulls newest complaints, regenerates a "top new issues" report. The "runs itself" story.
- **Level 3 — Alerting (stretch):** email/Slack alert when a new issue spikes. Also free.

**What it means (theory):**
- **Streamlit** — a Python library that turns a script into a shareable web app with no web-dev.
- **GitHub Actions** — free automation that runs your code on a schedule or on events.
- **On-demand vs scheduled** — on-demand = runs when a human asks; scheduled = runs by itself.

**Interview angle:**
- Q: "How would this work in production / how is it automated?"
  A: "Two modes — an on-demand upload app for ad-hoc analysis, and a scheduled GitHub Actions job
  that refreshes the report automatically. It's fully serverless and free-tier, so it's realistic
  for a small team to actually run."

**Mistakes / gotchas:** Don't build the fancy platform before the core engine is proven. Build &
validate the engine first, then wrap it. (Foundation before polish.)

---

## Entry 005 — Profiling the data BEFORE building (EDA) + real findings
**Date:** 2026-07-22 · **Context:** Project 1, understanding the CFPB data

**What we did:** Before any modelling, we profiled the FULL 8.5 GB file in memory-safe chunks
to answer: how big? how much usable text? what date range? which products? what's messy?

**Why we did it (PRINCIPLE):** "Understand your data before you touch it." This is called
**EDA (Exploratory Data Analysis)**. Skipping it is how analysts draw wrong conclusions.

**What it means (theory):**
- **EDA** — the first step of any data project: look at size, structure, distributions, missing
  values (nulls), and quirks, so you know what you're actually dealing with.
- **Chunked / out-of-core processing** — reading a file in small batches so it never has to fit
  in RAM all at once. Essential when data > memory (here 8.5 GB).
- **tz-naive vs tz-aware dates** — a real gotcha: some timestamps carry a timezone, some don't,
  and they can't be compared directly. Fix: normalize all to UTC then drop tz.

**The real findings (interview-ready facts):**
- 17.1M total complaints; 3.8M (22.3%) have narrative text; range Dec-2011 -> Jul-2026.
- Narratives only exist from 2015 onward (CFPB started publishing them then) -> the oldest rows
  look "empty," which is why judging data from the first chunk is misleading.
- Volume is exploding recently (2025 alone: ~1.2M narratives).
- **Product labels are MESSY:** the same real product appears under multiple names over the years
  (e.g. "Credit card" vs "Credit card or prepaid card"; three different "Credit reporting" labels).
  This must be cleaned by MERGING equivalent labels. Trusting raw labels blindly = a mistake.

**Interpretation:** We have far more than enough real text. Credit-card complaints (~233k across
two labels) are the sweet spot for our scope: rich, relatable, banking-relevant, right size.

**Interview angle:**
- Q: "How did you understand your data?"
  A: "I profiled the full 8.5 GB file with chunked processing — total volume, % with usable text,
  date coverage, product distribution, and null patterns — before modelling. That's how I caught
  that narratives only start in 2015 and that product labels were inconsistent and needed merging."
- Q: "What data-quality issues did you find?" A: inconsistent categorical labels (same product,
  many names), lots of nulls in some columns (Tags ~97% empty), and mixed timezone dates.

**Mistakes / gotchas:**
- Judging the dataset from the first 100k rows gave a false "0.7% have text" — the file is
  oldest-first. Lesson: always profile the WHOLE file, or a random sample, not just the top.
- Category labels drift over time in long-running public datasets → always check value_counts.

## Entry 006 — A real debugging story: silently corrupted dates (+ CSV vs Parquet)
**Date:** 2026-07-22 · **Context:** Project 1, extracting the working slice

**What happened:** After extracting our 125k credit-card slice, the "complaints per month"
chart showed a flat line. We did NOT ignore it (Rule: sanity-check everything). Investigating,
we found only ~6,281 of 124,962 dates were valid — the rest were NaT (missing). The data was
silently corrupted.

**How we debugged it (the method matters for interviews):**
1. Compared the chart to raw monthly counts → confirmed the anomaly was real, not cosmetic.
2. Scanned the full file for the TRUE year distribution → 2023:32k, 2024:35k, 2025:41k, 2026:16k
   (a healthy spread) — so the source data was fine; our slice was wrong.
3. Tested reading all 16 columns vs 3 columns → both fine → reading wasn't the cause.
4. Inspected the saved file → first rows had valid dates, middle rows were all NaT → pointed to
   a per-chunk type inconsistency that broke during `pd.concat`.
5. Root cause: across an 8.5 GB CSV, pandas inferred the date column's type differently in
   different chunks; concatenating mixed-type columns coerced many values to NaT.

**The fix:** convert the date column to a proper datetime INSIDE each chunk (before concat), so
every chunk stores the same clean type. After the fix: 124,962/124,962 valid dates. ✅

**Bonus fix — CSV → Parquet:** we also switched the saved slice from CSV to **Parquet** because
the narratives contain commas, quotes, and line breaks that make CSV fragile. Parquet stores text
safely, preserves data types, and is smaller (176 MB CSV → 74 MB Parquet).

**What it means (theory):**
- **Parquet** — a columnar binary file format; robust for messy text, typed, compressed, fast.
- **Type inference across chunks** — pandas guesses column types per chunk; guesses can differ,
  causing silent corruption on concat. Fix: set types explicitly / convert per chunk.
- **NaT** — pandas' "Not a Time" = a missing/invalid datetime.

**Interview angle:**
- Q: "Tell me about a bug you caught in your data." 
  A: "A time-series chart looked flat, which didn't match the source. I traced it to dates being
  silently corrupted during chunked extraction — pandas inferred the date column's type
  differently across chunks and concat coerced them to NaT. I fixed it by typing dates per chunk
  and switched storage from CSV to Parquet for robustness. Lesson: always sanity-check a result
  that looks off, and never trust a large CSV round-trip for free-text data."
- Q: "Why Parquet over CSV?" A: robust with delimiters/newlines in text, typed, compressed, faster.

**Mistakes / gotchas (the whole point):**
- Don't ignore a chart that looks 'off' — it saved us from building on corrupt data.
- Converting dates only AFTER concat was too late; per-chunk typing is the fix.
- CSV is risky for free text; prefer Parquet for storing text datasets.
- We had NOT deleted the 8.5 GB source yet — verifying before deleting is why we could re-extract.

## Entry 007 — The validate-everything principle (data is sacred)
**Date:** 2026-07-22 · **Context:** Project 1 — made a permanent working rule

**What we did:** Turned "always analyze and validate data thoroughly" into a permanent rule
(Rule 11) AND a reusable tool (`data_checks.py`) we run after every data operation.

**Why we did it:** The data is the foundation. If it's wrong/missing/uncleaned/misunderstood,
everything built on it is wasted. We caught a real corruption bug in Phase 1 by validating —
proof that this discipline matters.

**What it means (theory) — the validation cycle:**
Profile → check completeness (nulls) → check validity (sane values, valid dates) →
check quality (duplicates, inconsistent labels) → understand the source →
extract/transform → RE-VALIDATE the output against what we intended → only then move on.

**Key definitions:**
- **Data validation** — systematically confirming data meets expected structure, completeness,
  and correctness before using it.
- **Null / missing value** — an empty cell; too many in a column = don't trust that column.
- **Data quality dimensions** — completeness, validity, consistency, uniqueness, accuracy, timeliness.

**Interpretation:** Our clean slice passed: 124,962 rows, 0 duplicates, 0 empty narratives,
all dates valid (2023–2026), only known issue = 2 product labels to merge.

**Interview angle:**
- Q: "How do you ensure data quality?"
  A: "I profile and validate at every step — completeness, validity, consistency, duplicates —
  and re-validate after every transformation to confirm it did what I intended. I even built a
  reusable validation function so the check is consistent and never skipped."
- Q: "Why validate AFTER transforming, not just before?"
  A: "Because transformations can silently corrupt data — I learned this when a chunked
  extraction quietly broke my dates. The output must be re-checked, not assumed correct."

**Mistakes / gotchas:** The biggest risk is *assuming* a step worked. Always re-validate output.

## Entry 008 — Git & GitHub: the stage → commit → push cycle
**Date:** 2026-07-22 · **Context:** Phase 1 checkpoint — first push

**What we did:** Pushed Phase 1 to GitHub (repo: Complaint-Analysis-Report).

**What it means (theory) — the 3 stages, like shipping a package:**
- **Stage (`git add`)** — put chosen files "into the box" (mark what to save).
- **Commit (`git commit -m "message"`)** — seal & label the box; a save point ON YOUR COMPUTER.
- **Push (`git push`)** — ship the box to GitHub (the internet). This creates the green square.
- Key: commit ≠ push. Commit is local; push uploads. You can commit many times, push once.

**Useful terms:**
- **repository (repo)** — the project's folder tracked by Git.
- **branch / main** — a line of work; `main` is the primary one.
- **origin** — the nickname for the remote GitHub repo (the "address").
- **`.gitignore`** — lists files Git must NEVER upload (here: `.venv`, the 8.5GB data, the parquet).

**Interpretation of the success line:** `9398eae..d071a68  main -> main` = the commit moved from
local to GitHub. Only 129 KiB uploaded because data/venv were correctly ignored.

**Interview angle:**
- Q: "How do you use version control?"
  A: "Git with a phase-by-phase commit history; I keep large data and environments out via
  .gitignore, and push meaningful commits so the history tells the story of how the project evolved."
- Q: "Why not commit the dataset?" A: it's large and re-downloadable; repos should stay light and
  contain code, not big data or secrets.

**Mistakes / gotchas:** Never commit big data files, virtual environments, or secrets/API keys.
Always check `git add --dry-run` / `git check-ignore` before the first push of a new project.

## Entry 009 — Phase 2: cleaning text for NLP (without destroying meaning)
**Date:** 2026-07-22 · **Context:** Project 1, Phase 2

**What we did:** Cleaned 124,962 raw complaints into 112,481 clean, unique, model-ready ones.

**Why we did it:** NLP groups text by meaning. Noise (privacy masks) and duplicates would make
themes fuzzy and inflate counts. Clean input = trustworthy output.

**What we did, evidence-first:** we PROFILED the issues before cleaning and found:
- 12,268 exact-duplicate narratives (~10%) → would fake-inflate theme counts → removed.
- 75.9% of narratives contain `XXXX` privacy masks (median 4 each) → normalized, not deleted.
- 42.5% contain money masks `{$70.00}`; many have `XX/XX/year>` redacted dates.
- 256 narratives < 50 chars (low signal) → dropped (we chose the conservative <50 threshold).

**How we cleaned (careful, not aggressive):** replaced masks with neutral placeholders
(`<redacted>`, `<date>`, `<money>`) so the surrounding real sentence stays intact; merged the two
product labels ("Credit card" + "Credit card or prepaid card") into one; kept the ORIGINAL text
in its own column alongside the cleaned one (before/after always available).

**What it means (theory):**
- **Text preprocessing / normalization** — standardizing raw text so a model sees signal, not noise.
- **Regular expressions (regex)** — pattern rules to find/replace text (e.g. `X{2,}` = 2+ X's).
- **De-duplication** — removing repeated records so frequency counts are honest.
- **Why placeholders, not deletion?** removing masked tokens entirely can break sentences and lose
  context; a neutral token preserves grammar and meaning while removing identity noise.

**Interpretation:** 124,962 → 112,481 rows; single 'Credit card' label; validation passed.

**Interview angle:**
- Q: "How did you preprocess the text?"
  A: "Evidence-first: I profiled the noise (privacy masks, duplicates, short texts), then cleaned
  conservatively — normalized redaction masks to neutral placeholders to keep sentence meaning,
  removed ~10% exact duplicates that would have inflated theme frequencies, merged inconsistent
  product labels, and kept the raw text for auditability. Then I re-validated."
- Q: "Why not just delete all the XXXX?" A: it would fragment sentences and lose context; a
  placeholder preserves structure while removing the identity noise.

**Mistakes / gotchas:** Over-cleaning destroys signal. Always keep the raw text. Always
re-validate after cleaning (we confirmed 0 duplicates + single label post-clean).

## Entry 010 — Two working principles: show real examples + visualize
**Date:** 2026-07-22 · **Context:** made permanent (Rules 12 & 13)

**What we did:** Adopted two habits for every phase going forward:
1. **Validate with REAL examples** — always show a concrete before → after from the actual data,
   not just summary numbers. (e.g. Phase 2 shows 3 real complaints raw vs cleaned.)
2. **Visualize generously** — add clear, simple charts wherever they aid understanding, each with
   a one-line interpretation.

**Why:** tangible proof beats claims; a picture often explains more than a paragraph. Both make
the work easier to understand now AND easier to defend in an interview.

**Interview angle:**
- Q: "How do you make your analysis trustworthy/communicable?"
  A: "I demonstrate each step on real examples (before/after) and visualize the impact, so results
  are verifiable and easy to explain to non-technical stakeholders — not just numbers on a slide."

**Note:** these are now Rules 12 & 13 in the master plan; Kiro applies them automatically.

## Entry 011 — Phase 3: embeddings + clustering (the NLP engine core)
**Date:** 2026-07-22 · **Context:** Project 1, Phase 3 on 18k sample

**What we did:** Turned 18,000 cleaned complaints into meaning-vectors (embeddings), then grouped
them into 12 themes (clustering), and described each theme with keywords + real examples.

**Plain-English theory:**
- **Embedding** — turning each complaint into a list of numbers (here 384) that captures its
  MEANING, so similar complaints get similar numbers ("a location on a meaning-map"). Model:
  sentence-transformers `all-MiniLM-L6-v2`. Slow on CPU (~12 min for 18k) -> we saved the vectors.
- **Clustering** — finding the natural crowds of dots on that map; each crowd = a theme. We used
  **KMeans** (splits points into K groups). K=12 here.
- **TF-IDF** — a score that highlights words common in ONE theme but rare overall -> used to label
  each theme with its distinctive keywords.

**Result (real themes found):** fraud/unauthorized charges (13%), merchant disputes/refunds,
billing-error disputes, card declined/usability, credit reporting, prepaid/gift-card balance,
balance-transfer/interest, account closed without warning, identity theft, autopay failures,
rewards/points disputes, late-payment reporting. All business-sensible and defensible.

**Interview angle:**
- Q: "How did you find the themes without labels?" A: "Unsupervised learning — I embedded the
  complaints with a sentence-transformer, then clustered the vectors with KMeans, and labelled
  each cluster with its top TF-IDF terms plus example complaints."
- Q: "How do you choose K (number of clusters)?" A: start reasonable, inspect coherence, adjust;
  can use metrics (silhouette) or a method like HDBSCAN that finds clusters automatically.

**Mistakes / gotchas (found honestly):**
- Privacy placeholders ("redacted", "date", "money") leaked into the keyword labels as noise ->
  add them to the stopword list so theme labels are clean.
- Some themes overlap (two "dispute" clusters) -> normal; tune K or use better labeling.
- KMeans needs K chosen up front and assumes round-ish clusters; alternatives exist (HDBSCAN).

## Entry 012 — Severity scoring + priority ranking (business judgment)
**Date:** 2026-07-22 · **Context:** Project 1, Phase 3

**What we did:** Added a SEVERITY dimension so themes are ranked by PRIORITY (common AND severe),
not just volume. Built a priority-matrix chart.

**How severity was measured (two honest signals):**
1. **Negativity** — VADER sentiment (lexicon-based, fast, no API) on each complaint; compound
   score mapped to 0..1 where 1 = most negative.
2. **High-stakes words** — share of complaints mentioning serious terms (fraud, unauthorized,
   stolen, identity, threat, legal...).
   theme_severity = average of the two. priority = volume_share(%) x severity.

**What it means (theory):**
- **Sentiment analysis** — estimating emotional tone of text. VADER = a rule/lexicon method
  (fast, transparent) vs model-based sentiment (slower, sometimes more accurate).
- **Priority matrix** — a 2x2 business tool: impact (severity) vs frequency (volume); top-right
  = high/high = act first.

**Result:** Fraud ranked #1 (common + most severe). Identity theft rose despite lower volume (high
severity). Rewards/points fell to last (common but low severity). This matches real business logic.

**Interview angle:**
- Q: "How did you prioritize the problems?" A: "Not by volume alone - I combined frequency with a
  severity score (sentiment negativity + high-stakes keyword share) into a priority index, and
  visualized it as a frequency-vs-severity matrix so the 'fix-first' items are obvious."
- Q: "Why VADER not a deep model?" A: fast, transparent, no GPU/API; good enough as a severity
  proxy for prototyping. A transformer sentiment model is a possible upgrade.

**Mistakes / gotchas:** severity here is a PROXY (lexicon + keywords), not ground truth. Be honest
about that. VADER can misread sarcasm/formal text; the keyword list is hand-picked. Defensible for
a prototype, and we state its limits.

## Entry 013 — LLM-powered theme naming (GenAI in the pipeline)
**Date:** 2026-07-22 · **Context:** Project 1, Phase 3

**What we did:** Used Google Gemini (free tier, model gemini-flash-lite-latest) to turn each
theme's keywords + real example complaints into a crisp professional NAME + one-line description.
Replaced keyword-joins ("Company / Received / Payment") with names like "Payment Processing &
Account Management".

**How it works:** for each theme, send top keywords + 3 example complaints to the LLM, ask for
JSON {name, description}. Fallback to keyword-name if a call fails. Key read safely from .env.

**What it means (theory):**
- **API key** — a secret token that authenticates our requests to a paid/free web service. Kept
  in .env (git-ignored), never hard-coded or committed.
- **Prompt** — the instruction we send the LLM; we ask for strict JSON so the output is parseable.
- **Fallback / graceful degradation** — if the AI call fails, we still produce a usable name from
  keywords, so the pipeline never breaks.
- **This is the "GenAI" signal** in the project: embeddings+clustering (classic ML) + an LLM for
  labeling = a modern hybrid pipeline.

**Interview angle:**
- Q: "Where did you use GenAI / an LLM?" A: "For theme labeling — I fed each cluster's keywords
  and sample complaints to Gemini and asked for a concise name and description in JSON, with a
  keyword-based fallback if the API failed. So the heavy lifting is done by embeddings+clustering,
  and the LLM adds a human-readable layer on top."
- Q: "How do you keep API keys safe?" A: ".env file loaded at runtime, git-ignored; never in code
  or the repo."

**Mistakes / gotchas:** model names change over time (gemini-1.5/2.5 retired for new keys) -> list
available models rather than hard-code. Free tier has rate limits (429) -> pace calls (sleep) and
add a fallback. Some themes overlapped (fraud spread across 3 clusters) -> note honestly; could
reduce K or merge.

## Entry 014 — Scaling to the full 112k (more data = cleaner themes)
**Date:** 2026-07-22 · **Context:** Project 1, Phase 3 scaled to full dataset

**What we did:** Ran the full pipeline on ALL 112,481 complaints (embeddings ~75 min on CPU, then
clustering + severity + priority + LLM naming in a few minutes).

**Key finding (great interview point):** With 6x more data than the sample, the themes separated
MORE CLEANLY. In the 18k sample, "fraud" spread messily across ~3 overlapping clusters. In the
full 112k, they became distinct, sensible categories: Unauthorized Charges, Identity Theft,
Unauthorized Applications, Account Closures & Fraud. Lesson: more data -> more stable, reliable
clusters (KMeans centroids are estimated from more points, so groupings are less noisy).

**Final top problems (112k):** #1 Unauthorized Charges & Fraud (13.4% vol, severity 0.78 - most
common AND most severe), #2 Billing/Merchant Disputes, #3 Inaccurate Credit Reporting, #4 Payment
Processing errors, #5 Unauthorized Applications, #6 Identity Theft...

**Interview angle:**
- Q: "Did your results change at scale?" A: "Yes - on the full 112k the clusters were cleaner and
  more distinct than on an 18k sample; fraud sub-types that overlapped in the sample separated
  properly. More data reduced clustering noise. The business headline stayed consistent: fraud and
  disputes dominate."
- Q: "How did you make the big embedding job practical?" A: "Computed embeddings once (~75 min),
  saved them to disk, then all downstream analysis reloads them in seconds - separating the
  expensive step from the fast, iterative analysis."

**Mistakes / gotchas:** Running a 75-min job as one script is risky; we split embedding (save) from
analysis so a failure downstream never wastes the expensive step. Ran heavy jobs in the user's own
terminal (Kiro's tool interrupts long runs).
