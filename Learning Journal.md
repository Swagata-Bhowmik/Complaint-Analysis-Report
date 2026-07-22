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
