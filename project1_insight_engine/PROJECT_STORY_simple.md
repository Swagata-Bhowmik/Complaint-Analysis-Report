# 📖 Project 1 — The Whole Story in Simple Words

> A plain-English walkthrough of everything we built and every tool/algorithm we used.
> Written to be understandable with zero prior knowledge. Read this before interviews.

---

## 🎯 The one-sentence goal
Take a huge pile of real customer complaints about credit cards, and make a computer
automatically figure out **the top problems people face** — ranked by how common and how
serious they are — and eventually put it in an app anyone can use.

Think of it like this: a bank gets thousands of complaint letters. Nobody can read them all.
We built a machine that reads them and says "here are the 5 biggest problems, fix these first."

---

## 🧰 The basic tools (our "kitchen equipment")

- **Python** — the language we write instructions in. Everything is written in Python.
- **Virtual environment (`.venv`)** — a private "room" holding just the tools this project needs,
  so nothing clashes with other projects. Like a separate toolbox per project.
- **VS Code** — the app where we write and run our code (our workbench).
- **Jupyter Notebook (`.ipynb`)** — a special document where code runs in small blocks ("cells"),
  and you see the result right under each block. Great for learning step by step.
- **pandas** — the #1 tool for working with data tables (like Excel, but in code). A table in
  pandas is called a **DataFrame**.
- **Git + GitHub** — Git saves snapshots of our work; GitHub puts them online so recruiters can
  see the project. Each save = a "commit"; sending it online = a "push".
- **Parquet** — a file format for storing data tables. Better than CSV for our case: it keeps
  data types correct, handles messy text safely, and is smaller. (CSV broke our dates once;
  Parquet fixed it.)

---

## 🗂️ The data (our raw material)

- **CFPB** = the U.S. Consumer Financial Protection Bureau, a government body. They publish a
  free, public database of real complaints people filed about banks and credit cards.
- We used their file: **8.5 GB, 17 million complaints.** Way too big to open normally.
- The key column is the **"narrative"** — the actual story the customer wrote ("what happened").
- We chose **credit-card complaints from 2023 onward that have a written narrative.**

---

## 🏗️ Phase 1 — Understand the data (EDA)

- **EDA = Exploratory Data Analysis** = looking at your data BEFORE doing anything, to understand
  it: how big, what's in it, what's missing, what's weird. Skipping this = building on sand.
- **Chunking (out-of-core processing)** — the file was 8.5 GB, too big for the computer's memory
  (RAM). So instead of opening it all at once, we read it in small **chunks** (batches of rows),
  processed each, and threw it away. Like drinking a lake through a straw instead of all at once.
- **Null / missing value** — an empty cell. We counted how many each column had. Some columns
  (like "Tags") were almost always empty, so we ignored them.
- We carved out a smaller clean file of ~125,000 credit-card complaints from the giant file.
- **Bug we caught:** our dates got silently corrupted during extraction (a data-type mix-up when
  joining chunks). We noticed a chart looked wrong, investigated, and fixed it. Lesson: never
  trust a result that looks "off"; always sanity-check.

---

## 🧹 Phase 2 — Clean the text

The raw complaints were messy. We cleaned them so the computer could understand them:

- **Duplicates** — the exact same complaint appeared ~12,000 times. Duplicates lie about how
  common a problem is, so we removed them (kept one copy of each).
- **Privacy masks** — the government blacks out names/numbers as `XXXX`, dates as `XX/XX/year>`,
  and money as `{$70.00}`. We replaced these with neat placeholders (`<redacted>`, `<date>`,
  `<money>`) instead of deleting them — so the real sentence stays readable but the noise is gone.
- **Regex (regular expressions)** — a mini-language of patterns for find-and-replace in text.
  We used it to spot and swap the masks (e.g. "any run of 2+ X's" = a redaction).
- **Merged labels** — the same product had two names ("Credit card" and "Credit card or prepaid
  card"). We merged them into one so it's not counted as two things.
- Result: **112,481 clean, unique complaints.** We kept the original text too, so we can always
  show before/after.

---

## 🧠 Phase 3 — The engine (this is the exciting part)

This is where the computer actually "reads" the complaints and finds the problems. Four steps:

### Step 1 — Embeddings ("give each complaint a location on a meaning-map")
- Computers don't understand words, only numbers. So we turn each complaint into a list of
  **384 numbers** that represents its **meaning**. That list of numbers is called an
  **embedding** (or a **vector**).
- The rule: complaints that *mean* similar things get similar numbers, so they sit close together
  on an imaginary "meaning map." "I was charged twice" and "I got double-billed" land near each
  other even though the words differ.
- **sentence-transformers** — the tool that does this. **all-MiniLM-L6-v2** — the specific small
  AI model we used (it's free, fast, and good). "MiniLM" = a mini language model.
- This is the slow step (~12 min for 18k, ~75 min for 112k on our CPU) because it does deep math
  for every complaint. We **save** the results so we never redo it.

### Step 2 — Clustering ("circle the crowds on the map")
- Now every complaint is a dot on the meaning-map. **Clustering** = finding the crowds of dots.
  Each crowd = a group of similar complaints = a **theme** (a common problem).
- **KMeans** — the algorithm we used. In kid terms: you tell it "make K groups" (we picked
  K = 12). It drops 12 "flags" on the map, assigns each dot to its nearest flag, moves each flag
  to the middle of its dots, and repeats until the groups settle. Result: 12 tidy groups.
- **Why 12?** enough to separate distinct problems without splitting hairs. It's adjustable.

### Step 3 — Severity ("how bad is each problem?")
- Volume alone isn't enough; a business also cares how *serious* a problem is. We measured
  severity two ways:
  - **Sentiment / negativity** using **VADER** — a tool that reads text and scores how
    negative/positive it is (based on a dictionary of emotional words). Angry complaints score
    higher. ("Sentiment analysis" = judging the emotion/tone of text.)
  - **High-stakes words** — we counted complaints mentioning serious things (fraud, stolen,
    identity theft, legal...).
- **Priority = how common × how severe.** This gives a smart "fix-first" ranking, not just a
  popularity contest. (A "priority matrix" is a classic business chart: common+severe = top-right
  = do first.)

### Step 4 — Naming the themes ("give each crowd a human name")
- The groups were just "Theme 0, Theme 1..." We used an **LLM** (a large language model — an AI
  that understands and writes language) to give each theme a clean name + one-line description.
- **Gemini** — Google's LLM. We used the free tier via an **API** (a way for our code to talk to
  Google's AI over the internet). The secret **API key** lives in a hidden **.env** file that is
  never uploaded to GitHub (keeping it private).
- For each theme we sent the AI its keywords + 3 example complaints and asked for a short name.
  Example: "Theme 0" → **"Unauthorized/Fraudulent Charges."**

### Helper tools you'll want to know
- **TF-IDF** — a way to find the words that are *special* to one group (common inside the group
  but rare overall). We used it to pull each theme's keywords. (Stands for Term Frequency–Inverse
  Document Frequency — but just remember: "words that make this group distinctive.")
- **PCA** — a way to squash those 384 numbers down to 2 so we can draw the meaning-map on a flat
  picture. (It keeps the biggest patterns, loses tiny detail — good enough to visualize.)

---

## 📊 What we actually found (top credit-card problems)
1. **Unauthorized / fraudulent charges** (biggest AND most severe → fix first)
2. Merchant purchase & refund disputes
3. Credit-reporting & account disputes
4. Payment processing & account management
5. ...and more (account closures, identity theft, fees, rewards not given, etc.)

---

## 🔜 What's next
- **Scaling** — re-run the engine on ALL 112k complaints (not just an 18k sample) for stronger,
  more reliable results.
- **Phase 4 — the app (Streamlit):** a web page where someone uploads a complaints file and gets
  this whole analysis back automatically. **Streamlit** = a tool that turns Python into a website
  with almost no extra work.
- **Phase 5 — automation:** make it refresh by itself on a schedule (using GitHub Actions, a free
  robot that runs our code on a timer).

---

## 🗣️ If someone asks "what is this project?" — say this:
"I built a system that reads tens of thousands of real customer complaints and automatically
discovers the top problems, ranked by how common and how severe they are. It uses AI embeddings
to understand meaning, clustering to group similar complaints, sentiment scoring for severity, and
a language model to label each theme — delivered as an app where anyone can upload complaints and
get an instant, prioritized action list."
