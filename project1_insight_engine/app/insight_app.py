# =============================================================================
# INSIGHT ENGINE - Streamlit storytelling dashboard (light olive theme)
# =============================================================================
# A guided, chapter-by-chapter walkthrough of the whole project. Each chapter
# owns ONE distinct part of the story and goes deep on it - no page repeats
# another. Written so someone with zero ML/NLP background can follow it, learn
# the concepts, and defend every decision in an interview.
#
# RUN:  streamlit run project1_insight_engine/app/insight_app.py
# =============================================================================

import os
import sys
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

HERE = os.path.dirname(os.path.abspath(__file__))
NOTEBOOKS = os.path.join(HERE, "..", "notebooks")
DATA = os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "..", "outputs")
sys.path.insert(0, NOTEBOOKS)
from text_cleaning import clean_narrative

st.set_page_config(page_title="Insight Engine", page_icon="🔍", layout="wide")

# ---------------------------------------------------------------------------
# CSS - light olive/white, cards, badges, readable type.
# ---------------------------------------------------------------------------
st.markdown("""
<style>
.block-container {padding-top:1.6rem; padding-bottom:2rem; max-width:1180px;}
html, body, [class*="css"] {font-size:16px; color:#2E3320;}
.hero {background:linear-gradient(120deg,#7C9A3E 0%,#6B8E23 55%,#556B2F 100%);
       padding:26px 32px; border-radius:16px; margin-bottom:20px;
       box-shadow:0 8px 22px rgba(107,142,35,0.28);}
.hero h1 {color:#fff; font-size:1.95rem; margin:0 0 6px 0;}
.hero p {color:#F2F7E4; font-size:1.05rem; margin:0; line-height:1.5;}
.chapline {color:#7A8560; font-weight:700; letter-spacing:.6px; text-transform:uppercase;
           font-size:.78rem; margin:2px 0 10px 2px;}
.card {background:#F7FAEF; border:1px solid #DDE7C4; border-radius:14px; padding:18px 20px;
       height:100%; box-shadow:0 3px 10px rgba(85,107,47,0.08);}
.card .big {font-size:1.8rem; font-weight:800; color:#556B2F;}
.card .lbl {font-size:.8rem; color:#7A8560; text-transform:uppercase; letter-spacing:.5px;}
.problem {background:#F7FAEF; border-left:6px solid #6B8E23; border-radius:12px;
          padding:15px 20px; margin-bottom:12px; box-shadow:0 2px 8px rgba(85,107,47,0.07);}
.problem .rank {color:#6B8E23; font-weight:800; font-size:1.05rem;}
.problem .name {font-size:1.14rem; font-weight:700; color:#2E3320; margin:2px 0 6px 0;}
.problem .desc {color:#55603F; font-size:.95rem; margin-bottom:8px;}
.badge {display:inline-block; padding:3px 11px; border-radius:20px; font-size:.8rem;
        font-weight:700; margin-right:6px;}
.b-vol {background:#E3ECF7; color:#2C5C9E;} .b-sev {background:#F7E3E3; color:#B03A3A;}
.b-pri {background:#EAF0D9; color:#556B2F;}
.step {background:#F7FAEF; border:1px solid #DDE7C4; border-radius:14px; padding:18px 22px; margin-bottom:14px;}
.step .t {font-size:1.18rem; font-weight:800; color:#556B2F; margin-bottom:8px;}
.step .b {color:#3f4a2c; font-size:.98rem; line-height:1.6;}
.concept {background:#FffDF2; border:1px solid #E8DFA6; border-left:5px solid #C9A227;
          border-radius:10px; padding:12px 16px; margin:10px 0;}
.concept .h {font-weight:800; color:#9A7B0A;}
.concept .b {color:#5f5320; font-size:.95rem; line-height:1.55;}
.tool {background:#fff; border:1px solid #DDE7C4; border-left:5px solid #8FB04E; border-radius:10px;
       padding:12px 16px; margin-bottom:10px;}
.tool .n {font-weight:700; color:#556B2F;}
.tool .d {color:#4a552f; font-size:.94rem;}
.pill {display:inline-block; background:#EAF0D9; color:#556B2F; padding:4px 12px; border-radius:16px;
       font-size:.85rem; font-weight:600; margin:3px 4px 3px 0;}
.qa {background:#F4F7EC; border:1px solid #DDE7C4; border-radius:10px; padding:12px 16px; margin-bottom:10px;}
.qa .q {font-weight:800; color:#3E4A22;}
.qa .a {color:#45512b; font-size:.95rem;}
h3 {margin-top:1.4rem !important; color:#3E4A22;}
blockquote {border-left:4px solid #6B8E23; background:#F2F5E9; padding:8px 16px; border-radius:6px; color:#3f4a2c;}
code {background:#EEF2E0; color:#4F6B1C; padding:1px 5px; border-radius:4px;}
</style>
""", unsafe_allow_html=True)

PLOTLY = dict(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
              font_color="#2E3320", margin=dict(t=30, r=20, l=20, b=20))
GREENS = ["#DCE8B8", "#B5CC7A", "#8FB04E", "#6B8E23", "#4F6B1C", "#3B5015"]


@st.cache_data(show_spinner=False)
def load_full_results():
    """Load the compact deploy bundle (works locally AND on hosted GitHub deploy).
    Returns (themes_df, total_complaints, examples_by_theme)."""
    import json
    with open(os.path.join(HERE, "deploy_data.json"), encoding="utf-8") as f:
        bundle = json.load(f)
    rows, examples = [], {}
    for t in bundle["themes"]:
        rows.append({"rank": t["rank"], "theme": t["theme"], "name": t["name"],
                     "description": t["description"], "share_%": t["share_pct"],
                     "severity": t["severity"], "priority": t["priority"]})
        examples[t["theme"]] = t["examples"]
    themes = pd.DataFrame(rows).sort_values("rank")
    return themes, int(bundle["total_complaints"]), examples

@st.cache_resource(show_spinner=False)
def load_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")

def sev_label(v):
    return "High" if v >= 0.5 else ("Medium" if v >= 0.35 else "Low")

def card(col, label, value, small=False):
    fs = "1.15rem" if small else "1.8rem"
    col.markdown(f'<div class="card"><div class="lbl">{label}</div>'
                 f'<div class="big" style="font-size:{fs};">{value}</div></div>', unsafe_allow_html=True)

def step(title, body):
    st.markdown(f'<div class="step"><div class="t">{title}</div><div class="b">{body}</div></div>',
                unsafe_allow_html=True)

def concept(term, body):
    st.markdown(f'<div class="concept"><span class="h">💡 {term}</span><div class="b">{body}</div></div>',
                unsafe_allow_html=True)

def tool(name, desc):
    st.markdown(f'<div class="tool"><span class="n">{name}</span> — <span class="d">{desc}</span></div>',
                unsafe_allow_html=True)

def qa(q, a):
    st.markdown(f'<div class="qa"><div class="q">Q. {q}</div><div class="a">{a}</div></div>',
                unsafe_allow_html=True)

def chapter(label):
    st.markdown(f'<div class="chapline">{label}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------
def chart_ranked_bars(themes):
    t = themes.sort_values("priority")
    fig = px.bar(t, x="priority", y="name", orientation="h", color="severity",
                 color_continuous_scale=GREENS, text="priority",
                 labels={"priority": "Priority (volume × severity)", "name": "", "severity": "Severity"})
    fig.update_traces(textposition="outside")
    fig.update_layout(height=520, **PLOTLY)
    return fig

def chart_treemap(themes):
    fig = px.treemap(themes, path=["name"], values="share_%", color="severity",
                     color_continuous_scale=GREENS, custom_data=["share_%", "severity", "priority"])
    fig.update_traces(hovertemplate="<b>%{label}</b><br>Volume: %{customdata[0]}%<br>"
                                     "Severity: %{customdata[1]}<br>Priority: %{customdata[2]}<extra></extra>",
                      textinfo="label+percent entry")
    fig.update_layout(height=520, **PLOTLY)
    return fig

def chart_matrix(themes):
    t = themes.copy(); t["rank"] = t["rank"].astype(int)
    fig = px.scatter(t, x="share_%", y="severity", size="priority", color="priority",
                     text=t["rank"].astype(str), color_continuous_scale=GREENS, size_max=55,
                     custom_data=["name", "description", "share_%", "severity", "priority"],
                     labels={"share_%": "Volume (%)", "severity": "Severity (0–1)"})
    fig.update_traces(textposition="middle center",
                      textfont=dict(size=13, color="white", family="Arial Black"),
                      hovertemplate="<b>#%{text} %{customdata[0]}</b><br>%{customdata[1]}<br><br>"
                                    "Volume: %{customdata[2]}%<br>Severity: %{customdata[3]}<br>"
                                    "Priority: %{customdata[4]}<extra></extra>")
    fig.add_vline(x=t["share_%"].median(), line_dash="dash", line_color="#9AA77A")
    fig.add_hline(y=t["severity"].median(), line_dash="dash", line_color="#9AA77A")
    fig.update_layout(height=560, **PLOTLY)
    return fig


# ===========================================================================
# CHAPTER 0 - HOME  (owns: the pitch + the map of the journey)
# ===========================================================================
def page_home():
    st.markdown('<div class="hero"><h1>🔍 Insight Engine</h1>'
                '<p>An AI system that reads tens of thousands of real customer complaints and '
                'automatically tells you the <b>top problems to fix</b> — ranked by how common and '
                'how serious they are. Built end-to-end on real public data.</p></div>',
                unsafe_allow_html=True)
    themes, total, examples = load_full_results()
    c1, c2, c3, c4 = st.columns(4)
    card(c1, "Complaints analyzed", f"{total:,}")
    card(c2, "Themes discovered", f"{themes['theme'].nunique()}")
    card(c3, "Raw data processed", "8.5 GB")
    card(c4, "#1 problem", themes.iloc[0]["name"], small=True)

    st.markdown("### 👋 The whole idea in 30 seconds")
    st.markdown(
        "A bank gets **thousands of complaint letters a week** — double charges, fraud, app crashes, "
        "rude service. No human can read them all, so the single most valuable piece of information — "
        "*what is actually going wrong* — stays buried. Managers end up guessing.\n\n"
        "This project builds a machine that **reads every complaint**, groups the similar ones into "
        "**themes**, scores how **serious** each theme is, and hands back a ranked list: "
        "*“here are the top problems, fix these first.”* No labels were given to it — it discovered "
        "the themes on its own.")

    st.markdown("### 🧭 How to read this dashboard (it's a story, in order)")
    st.markdown(
        "Each chapter in the sidebar owns **one distinct part** of the journey — nothing is repeated. "
        "Read them top to bottom and the whole project unfolds like a story:")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            "1. **🎯 The Problem** — the business pain and what success looks like.\n"
            "2. **🗂️ The Data** — where the data came from and what exploring it taught us.\n"
            "3. **🧹 Cleaning** — how we turned messy text into trustworthy input.\n"
            "4. **🧠 The AI Engine** — *the teaching chapter*: how a computer 'reads' text, in plain words.\n"
            "5. **📊 The Results** — the actual top problems, with charts and real complaints.")
    with c2:
        st.markdown(
            "6. **📤 Analyze Your File** — run the engine live on your own complaints.\n"
            "7. **🛠️ Tech Stack** — every technology used, as a quick reference.\n"
            "8. **🎓 Discoveries** — the bugs we caught and lessons learned (great for interviews).\n"
            "9. **🚀 Next & Deploy** — automation, deployment, and how this ships to the world.")
    st.markdown("> **The one rule behind everything:** real public data only, no fabrication. "
                "Every single number in here traces back to a real complaint and can be defended step by step.")


# ===========================================================================
# CHAPTER 1 - THE PROBLEM  (owns: the business case)
# ===========================================================================
def page_problem():
    st.markdown('<div class="hero"><h1>🎯 Chapter 1 — The Problem & The Goal</h1>'
                '<p>Before any code: what business pain are we solving, and how will we know we won?</p></div>',
                unsafe_allow_html=True)
    chapter("This chapter owns: the business case — the 'why' behind the whole project")

    step("😖 The pain, concretely",
         "A bank receives <b>thousands of complaints every week</b> in free-form English. Each one is a "
         "story: a double charge, a fraudulent transaction, an app that failed, a rude agent. Reading "
         "them one-by-one is physically impossible, so the richest signal a company owns — "
         "<i>its customers telling it exactly what is broken</i> — is wasted. Teams end up reacting to "
         "whoever complains loudest, or to a gut feeling, not to what is actually most common and most damaging.")

    step("🎯 The three questions we must answer",
         "A useful system has to answer, automatically:<br>"
         "<b>1. What are people complaining about?</b> → discover the recurring themes.<br>"
         "<b>2. Which problems matter most?</b> → rank them by how <i>common</i> AND how <i>severe</i> they are.<br>"
         "<b>3. So what do we do first?</b> → a clear, ordered 'fix-first' list plus a tool anyone can reuse.")

    step("💼 Why this is worth money (business value)",
         "Turning raw text into a ranked action plan means the company fixes the <b>right</b> things first. "
         "That directly reduces refunds and chargebacks, lowers churn (customers leaving), cuts call-centre "
         "load, and protects brand trust. The difference this project captures is the difference between "
         "<i>“we ran an algorithm”</i> and <i>“we answered a business question that saves money.”</i>")

    step("✅ What 'success' looks like",
         "A stakeholder who has never seen the data can open one screen and instantly see: the top problems, "
         "in priority order, each with a plain-English name, real example complaints behind it, and a "
         "defensible reason it ranks where it does. That is exactly what the <b>📊 Results</b> chapter delivers.")

    st.markdown("> **Interview one-liner:** *“I built a system that turns raw customer complaints into a "
                "prioritized action plan — the top problems ranked by frequency and severity, delivered as "
                "a dashboard and a self-serve upload tool.”*")


# ===========================================================================
# CHAPTER 2 - THE DATA  (owns: sourcing, compliance, and EDA)
# ===========================================================================
def page_data():
    st.markdown('<div class="hero"><h1>🗂️ Chapter 2 — The Data</h1>'
                '<p>The foundation. If the data is wrong, everything built on it is wrong — so we chose it '
                'carefully and explored it thoroughly before writing a line of modelling code.</p></div>',
                unsafe_allow_html=True)
    chapter("This chapter owns: where the data came from, why it's legal, and what exploring it revealed")

    c1, c2, c3, c4 = st.columns(4)
    card(c1, "Full file", "17.1M rows")
    card(c2, "On disk", "8.5 GB")
    card(c3, "Have written text", "3.8M (22%)", small=True)
    card(c4, "Our final scope", "112,481", small=True)

    step("📚 What the data is",
         "The <b>CFPB Consumer Complaint Database</b> — published free by the U.S. Consumer Financial "
         "Protection Bureau (a government body). It contains real complaints people filed about banks and "
         "credit cards. The field that matters to us is the <b>narrative</b>: the customer's own written "
         "story of what happened. That free text is the raw material the whole engine runs on.")

    step("🧭 Why THIS data — and deliberately not scraping app reviews",
         "This was a compliance decision, not just a convenience one:<br>"
         "• <b>Legal & clean</b> — government open data is explicitly free to use. Scraping the Play Store / "
         "App Store <i>violates their terms of service</i>, can get you blocked, and pulls in personal data "
         "(privacy risk). <b>“Publicly visible” is not the same as “free and safe to bulk-collect.”</b><br>"
         "• <b>Large & real</b> — millions of genuine complaints, not a few hundred scraped reviews or "
         "synthetic AI-generated text (which can't be defended in an interview).<br>"
         "• <b>Problem-focused</b> — it's complaints, i.e. described problems, not star ratings. That's "
         "exactly what a 'what should we fix?' tool needs.")

    concept("EDA (Exploratory Data Analysis)",
            "Looking hard at your data <i>before</i> you build anything — how big it is, what's inside, what's "
            "missing, and what's weird — so you don't draw wrong conclusions later. Skipping EDA is how "
            "analysts quietly build on sand.")

    concept("Chunked / out-of-core processing",
            "The file is 8.5 GB — far too big to open all at once in memory (RAM). So we read it in small "
            "<b>chunks</b> of 200,000 rows, summarised each chunk, and discarded it before reading the next. "
            "Like drinking a lake through a straw instead of trying to swallow it whole. This is the "
            "professional way to profile data that's bigger than your computer's memory.")

    step("🔬 What profiling the full file actually told us",
         "<ul>"
         "<li><b>17.1M</b> total complaints; only <b>3.8M (22%)</b> have written narratives — because the "
         "narrative is opt-in.</li>"
         "<li>Narratives only exist from <b>2015 onward</b> (that's when CFPB started publishing them), so "
         "the oldest rows look empty. Judging the dataset from the first chunk gave a misleading '0.7% have "
         "text' — the file is stored oldest-first. <b>Lesson: profile the whole file, not just the top.</b></li>"
         "<li>Volume is exploding: 2025 alone had ~1.2M narratives.</li>"
         "<li><b>Product labels are messy</b> — the same real product appears under multiple names over the "
         "years (e.g. 'Credit card' vs 'Credit card or prepaid card'). Trusting raw labels blindly would "
         "double-count. They must be merged.</li>"
         "</ul>")

    step("🎯 How we narrowed 17M rows down to our working set",
         "We locked a clear scope: <b>Product = Credit card</b> (merging both label variants), "
         "<b>only rows with a narrative</b>, and <b>2023 onward</b> (recent, relevant). Filtering the giant "
         "file in chunks produced <b>124,962</b> credit-card complaints — the slice we then cleaned. "
         "Credit cards are the sweet spot: rich, relatable, banking-relevant, and the right size to run on a laptop.")

    st.markdown("> **Lesson to say out loud:** *“Understand your data before you touch it. Data sourcing and "
                "compliance matter as much as the modelling.”* The debugging story of how this data nearly "
                "tricked us lives in the **🎓 Discoveries** chapter.")


# ===========================================================================
# CHAPTER 3 - CLEANING  (owns: text preprocessing, in depth)
# ===========================================================================
def page_cleaning():
    st.markdown('<div class="hero"><h1>🧹 Chapter 3 — Cleaning the Text</h1>'
                '<p>Careful, evidence-first cleaning that removes noise without destroying meaning. '
                'Clean input is the only way to get trustworthy themes out the other end.</p></div>',
                unsafe_allow_html=True)
    chapter("This chapter owns: how raw messy text became model-ready — and why every choice was conservative")

    c1, c2, c3 = st.columns(3)
    card(c1, "Before cleaning", "124,962")
    card(c2, "Removed", "12,481")
    card(c3, "Clean & unique", "112,481")

    step("🔎 We measured the mess before touching it (evidence-first)",
         "Rather than guessing, we profiled the noise first and found:<br>"
         "• <b>12,268 exact-duplicate</b> narratives (~10%) — the same complaint text repeated.<br>"
         "• <b>75.9%</b> of narratives contain <code>XXXX</code> privacy masks (median 4 per complaint).<br>"
         "• <b>42.5%</b> contain money masks like <code>{$70.00}</code>; many contain <code>XX/XX/year&gt;</code> redacted dates.<br>"
         "• <b>256</b> narratives shorter than 50 characters (too little signal).")

    step("🧯 Why each of these is a problem",
         "<b>Duplicates</b> lie about how common a problem is — 12,000 copies of one complaint would fake-"
         "inflate a theme's size. <b>Privacy masks</b> (the government blacks out names/dates/money) are pure "
         "noise to a meaning model. <b>Two product labels</b> for one product would split one theme into two. "
         "<b>Ultra-short</b> texts carry almost no meaning to cluster on.")

    concept("Regular expressions (regex)",
            "A tiny pattern-matching language for find-and-replace in text. Example: the pattern "
            "<code>X{2,}</code> means 'two or more capital X's in a row' — that's how we detect a redaction "
            "like <code>XXXX</code> and swap it out, no matter how long it is.")

    step("🧼 What we did — carefully, not aggressively",
         "• Removed exact duplicates (kept one copy of each).<br>"
         "• Merged the two product labels into a single <code>Credit card</code> category.<br>"
         "• Turned privacy masks into <b>neutral placeholders</b> — <code>&lt;redacted&gt;</code>, "
         "<code>&lt;date&gt;</code>, <code>&lt;money&gt;</code> — instead of deleting them.<br>"
         "• Dropped the &lt;50-character texts.<br>"
         "• <b>Kept the original text in its own column</b>, so we can always show before/after and never lose the raw data.")

    concept("Why placeholders instead of just deleting the masks?",
            "If you delete every <code>XXXX</code>, sentences shatter: 'In &lt;date&gt; my &lt;redacted&gt; "
            "was charged' becomes 'In my was charged' — grammar and meaning gone. A neutral placeholder keeps "
            "the sentence readable and its meaning intact while removing the identity noise. "
            "<b>Over-cleaning destroys signal.</b>")

    st.markdown("**Real before → after (from the actual data):**")
    st.markdown('<blockquote><b>Before:</b> “In XX/XX/year&gt;, XXXX applied charges higher than I agreed…”'
                '<br><b>After:</b> “In &lt;date&gt;, &lt;redacted&gt; applied charges higher than I agreed…”'
                '</blockquote>', unsafe_allow_html=True)

    st.markdown("> **Lesson to say out loud:** *“I cleaned conservatively and re-validated after every step — "
                "clean just enough to remove noise, keep the raw text for auditability, and prove it worked "
                "on real examples, not just summary numbers.”*")


# ===========================================================================
# CHAPTER 4 - THE AI ENGINE  (owns: the ML/NLP concepts, taught from zero)
# ===========================================================================
def page_engine():
    st.markdown('<div class="hero"><h1>🧠 Chapter 4 — The AI Engine</h1>'
                '<p>The teaching chapter. This is where a computer actually “reads” complaints and finds the '
                'problems. Every concept is explained from zero — read this one slowly.</p></div>',
                unsafe_allow_html=True)
    chapter("This chapter owns: ALL the machine-learning concepts. Other chapters just refer back here.")

    st.markdown("The engine is a **5-step pipeline**. Each step feeds the next:")
    st.markdown('<span class="pill">1 · Embeddings</span><span class="pill">2 · Clustering</span>'
                '<span class="pill">3 · Keywords (TF-IDF)</span><span class="pill">4 · Severity</span>'
                '<span class="pill">5 · Priority</span><span class="pill">+ LLM naming</span>',
                unsafe_allow_html=True)

    # ---- STEP 1 ----
    st.markdown("### 🧠 Step 1 — Embeddings: give each complaint a location on a 'meaning-map'")
    step("The core idea",
         "Computers understand numbers, not words. So we turn each complaint into a list of "
         "<b>384 numbers</b> called an <b>embedding</b> (or a <b>vector</b>). The magic rule: complaints "
         "that <i>mean</i> similar things get similar numbers. So 'I was charged twice' and 'I got "
         "double-billed' land right next to each other — even though they share almost no words. Picture "
         "every complaint as a dot on a giant map where distance = difference in meaning.")
    concept("Embedding / vector",
            "A fixed-length list of numbers that captures the <i>meaning</i> of a piece of text. Think of it "
            "as a GPS coordinate in 'meaning-space'. Similar meaning → nearby coordinates.")
    concept("The model: all-MiniLM-L6-v2 (a sentence-transformer)",
            "A small, free, pre-trained AI model that produces those 384-number vectors. 'MiniLM' = a "
            "mini language model — small enough to run on a normal laptop CPU, good enough to capture "
            "meaning well. We didn't train it; we <i>used</i> it (that's called using a pre-trained model).")
    step("The practical reality",
         "Embedding is the slow step: ~12 minutes for an 18k sample, ~<b>75 minutes</b> for all 112k on a "
         "CPU, because it does deep math for every complaint. So we ran it <b>once</b> and saved the vectors "
         "to disk. Every later experiment reloads them in a second. This 'compute-once, reuse-forever' "
         "split is a real engineering decision — see <b>🎓 Discoveries</b>.")

    # ---- STEP 2 ----
    st.markdown("### 🧩 Step 2 — Clustering: circle the crowds on the map")
    step("The core idea",
         "Now every complaint is a dot on the meaning-map. <b>Clustering</b> means finding the natural "
         "crowds of dots. Each crowd is a group of similar complaints = a <b>theme</b> (a recurring problem). "
         "Crucially, nobody told the computer what the themes are — it discovers them itself. That's called "
         "<b>unsupervised learning</b> (learning with no answer key).")
    concept("KMeans (the clustering algorithm we used)",
            "You tell it 'make K groups' (we chose K=12). It drops 12 flags on the map, assigns each dot to "
            "its nearest flag, moves each flag to the centre of its assigned dots (the '<b>centroid</b>'), "
            "and repeats until the groups stop moving. Result: 12 tidy groups. The centroid is just the "
            "average position of a group.")
    concept("Why K = 12?",
            "Enough groups to separate genuinely different problems, without splitting hairs into dozens of "
            "near-identical slivers. It's a starting choice you inspect and can adjust. In the upload tool "
            "you can literally slide K yourself and watch the themes change.")

    # ---- STEP 3 ----
    st.markdown("### 🔤 Step 3 — TF-IDF: find the words that make each theme distinctive")
    concept("TF-IDF (Term Frequency – Inverse Document Frequency)",
            "A score that highlights words which are <i>common inside one theme but rare everywhere else</i>. "
            "Words like 'the' and 'card' appear everywhere, so they score low. A word like 'chargeback' that "
            "clusters in one theme scores high. We use the top-scoring words as each theme's keyword label — "
            "e.g. 'fraud / unauthorized / dispute'. In short: <b>the words that make this group special.</b>")

    # ---- STEP 4 ----
    st.markdown("### ⚠️ Step 4 — Severity: how bad is each problem, not just how common?")
    step("Why volume alone is not enough",
         "A theme can be huge but mild (e.g. 'rewards points confusion'), or smaller but devastating "
         "(e.g. 'identity theft'). A business cares about <b>both</b>. So we score how <i>serious</i> each "
         "complaint is, using two honest signals combined:")
    concept("Signal 1 — Sentiment negativity (VADER)",
            "<b>Sentiment analysis</b> = judging the emotional tone of text. <b>VADER</b> is a fast, "
            "dictionary-based tool: it knows which words are angry/negative and gives each complaint a "
            "'compound' score from -1 (very negative) to +1 (very positive). We flip that onto a 0–1 scale "
            "where 1 = most negative. No GPU, no API, fully transparent.")
    concept("Signal 2 — High-stakes keywords",
            "The share of complaints in a theme that mention genuinely serious words — <i>fraud, "
            "unauthorized, stolen, scam, identity, threat, legal, police, victim</i>. A theme full of these "
            "is objectively more severe.")
    step("Combining them",
         "<b>theme severity = average of (negativity) and (high-stakes share)</b>, both on a 0–1 scale. "
         "We're honest that this is a <i>proxy</i> for severity, not ground truth — VADER can misread "
         "sarcasm, and the keyword list is hand-picked. That's a perfectly defensible prototype choice, "
         "and stating its limits is a strength in an interview.")

    # ---- STEP 5 ----
    st.markdown("### 🏆 Step 5 — Priority: the smart ranking")
    step("The formula",
         "<b>Priority = Volume (%) × Severity.</b> This surfaces problems that are both common AND serious — "
         "not a popularity contest, not a fear contest. It's the classic business <b>priority matrix</b>: "
         "plot volume on one axis, severity on the other; the top-right corner (common + severe) is 'fix "
         "these first'. You can see that exact chart in <b>📊 Results</b>.")
    concept("A little statistics (nothing scary)",
            "The only stats here are the friendly kind: a <b>mean</b> (average) to combine the two "
            "severity signals, a <b>percentage share</b> for volume, and a <b>median</b> (the middle "
            "value) to draw the divider lines on the priority matrix. We also <b>normalise</b> scores to "
            "a 0–1 range before combining them, so one signal can't dominate just because it uses bigger "
            "numbers. That's it — no heavy maths required to understand the result.")

    # ---- LLM naming ----
    st.markdown("### 🏷️ Final touch — an LLM gives each theme a human name")
    step("From 'Theme 0' to 'Unauthorized Charges & Fraud Disputes'",
         "The groups start as bare numbers. We send each theme's top keywords + 3 real example complaints to "
         "an <b>LLM</b> and ask for a short name and one-line description, returned as strict JSON so our "
         "code can read it. If a call fails, we fall back to the TF-IDF keyword label — the pipeline never breaks.")
    concept("LLM (Large Language Model) — here, Google Gemini",
            "An AI that understands and writes human language. We used Gemini's free tier via an <b>API</b> "
            "(our code talking to Google's AI over the internet). The secret <b>API key</b> lives in a hidden "
            "<code>.env</code> file that is never uploaded to GitHub. This is the 'GenAI' layer: classic ML "
            "(embeddings + clustering) does the heavy lifting; the LLM just adds a readable label on top.")

    # ---- helper ----
    st.markdown("### 🧰 One more helper — PCA (only for the picture)")
    concept("PCA (Principal Component Analysis)",
            "Our vectors have 384 dimensions — impossible to draw. PCA squashes them down to 2 dimensions "
            "while keeping the biggest patterns, so we can plot the meaning-map as a flat scatter of dots. "
            "It loses tiny detail but keeps the overall shape — good enough to <i>see</i> the clusters.")

    st.markdown("> **The whole engine in one breath:** *embeddings turn text into meaning-vectors → KMeans "
                "clusters them into themes → TF-IDF labels each theme → VADER + keywords score severity → "
                "volume × severity ranks them → an LLM names them.*")


# ===========================================================================
# CHAPTER 5 - RESULTS  (owns: the findings + interpretation)
# ===========================================================================
def page_results():
    st.markdown('<div class="hero"><h1>📊 Chapter 5 — The Results</h1>'
                '<p>The top credit-card problems, discovered automatically from 112,481 real complaints. '
                'This is the payoff of every chapter before it.</p></div>', unsafe_allow_html=True)
    chapter("This chapter owns: the actual answers and how to read them")
    themes, total, examples = load_full_results()

    st.markdown("### 🔭 The headline")
    st.markdown(
        "The engine ranked 12 themes. The clear story: **fraud and disputes dominate**. "
        "**Unauthorized Charges & Fraud** is #1 — it is both the **most common (13.4%)** and the "
        "**most severe (0.78)** theme, which is the worst possible combination and an unambiguous "
        "'fix-first'. Billing/merchant disputes and credit-reporting errors follow. Low-severity themes "
        "like rewards confusion correctly sink to the bottom even though they're fairly common.")

    st.markdown("### 📈 Explore the ranking three ways")
    style = st.radio("Chart style:", ["Ranked bars", "Treemap (boxes)", "Priority matrix"], horizontal=True)
    if style == "Ranked bars":
        st.caption("Longer bar = higher priority (common × severe). Colour = severity.")
        st.plotly_chart(chart_ranked_bars(themes), use_container_width=True)
    elif style.startswith("Treemap"):
        st.caption("Box size = number of complaints. Darker green = more severe.")
        st.plotly_chart(chart_treemap(themes), use_container_width=True)
    else:
        st.caption("This is the priority matrix from Chapter 4. Bubbles numbered by rank. "
                   "Right = common, Up = severe. Top-right = fix first. Hover for detail.")
        st.plotly_chart(chart_matrix(themes), use_container_width=True)

    st.markdown("### 🏆 The ranked problems")
    for _, r in themes.iterrows():
        st.markdown(f'<div class="problem"><span class="rank">#{int(r["rank"])}</span> '
                    f'<span class="name">{r["name"]}</span><div class="desc">{r["description"]}</div>'
                    f'<span class="badge b-vol">📈 {r["share_%"]}% of complaints</span>'
                    f'<span class="badge b-sev">⚠️ Severity: {sev_label(r["severity"])} ({r["severity"]})</span>'
                    f'<span class="badge b-pri">🏆 Priority {r["priority"]}</span></div>', unsafe_allow_html=True)

    st.markdown("### 🔎 Read the real complaints behind any theme")
    st.caption("Proof, not claims: these are the actual customer narratives that landed in each cluster.")
    pick = st.selectbox("Choose a theme:", themes["name"].tolist())
    tid = int(themes[themes["name"] == pick].iloc[0]["theme"])
    for i, e in enumerate(examples.get(tid, []), 1):
        with st.expander(f"Example {i}"):
            st.write(str(e) + "…")


# ===========================================================================
# CHAPTER 6 - ANALYZE YOUR FILE  (owns: the live interactive tool)
# ===========================================================================
def page_analyze():
    st.markdown('<div class="hero"><h1>📤 Chapter 6 — Analyze Your Own Complaints</h1>'
                '<p>Everything from Chapter 4, running live. Upload a file of complaints → get an instant '
                'ranked breakdown. (Free demo analyses up to 1,500 rows.)</p></div>', unsafe_allow_html=True)
    chapter("This chapter owns: the hands-on demo — the engine you just learned about, working in real time")

    st.markdown("### 🧪 No file handy? Try the sample")
    st.caption("400 real CFPB credit-card complaints (never used in the 📊 Results) — a genuine end-to-end test.")
    try:
        with open(os.path.join(HERE, "sample_complaints_for_demo.csv"), "rb") as f:
            st.download_button("⬇️ Download sample complaints file (CSV)", f,
                               "sample_complaints_for_demo.csv", "text/csv")
    except FileNotFoundError:
        pass
    st.markdown("---")

    up = st.file_uploader("Upload complaints file (CSV or Excel)", type=["csv", "xlsx"])
    if up is None:
        st.info("👆 Upload a file with a column of complaint text to begin — or grab the sample above.")
        return
    df = pd.read_csv(up) if up.name.endswith(".csv") else pd.read_excel(up)
    st.success(f"✅ Loaded {len(df):,} rows.")
    col = st.selectbox("Which column has the complaint text?", df.columns.tolist())
    n_themes = st.slider("How many themes to find? (this is 'K' from Chapter 4)", 3, 12, 6)
    if not st.button("🚀 Analyze now"):
        return
    work = df[[col]].dropna().head(1500).copy(); work.columns = ["text"]
    work["clean"] = work["text"].astype(str).apply(clean_narrative)
    prog = st.progress(0, text="Step 1/3 — embeddings…")
    emb = load_model().encode(work["clean"].tolist(), show_progress_bar=False, batch_size=32)
    prog.progress(45, text="Step 2/3 — clustering…")
    from sklearn.cluster import KMeans
    from sklearn.feature_extraction.text import TfidfVectorizer
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    work["theme"] = KMeans(n_clusters=n_themes, random_state=42, n_init=10).fit_predict(emb)
    prog.progress(75, text="Step 3/3 — severity & ranking…")
    analyzer = SentimentIntensityAnalyzer()
    comp = work["text"].astype(str).apply(lambda t: analyzer.polarity_scores(t[:1000])["compound"])
    work["negativity"] = (1 - comp) / 2
    SEVERE = ["fraud", "unauthorized", "stolen", "scam", "theft", "identity", "threat", "legal"]
    work["severe"] = work["text"].str.contains("|".join(SEVERE), case=False, na=False).astype(int)
    vec = TfidfVectorizer(max_features=2000, stop_words="english", ngram_range=(1, 2))
    tfidf = vec.fit_transform(work["clean"]); terms = np.array(vec.get_feature_names_out())
    NOISE = {"redacted", "date", "money", "xxxx", "xx"}
    def kw(tid, n=3):
        rows = np.where(work["theme"].values == tid)[0]
        order = np.asarray(tfidf[rows].mean(axis=0)).ravel().argsort()[::-1]
        return " / ".join([terms[i] for i in order if terms[i] not in NOISE][:n]).title()
    g = work.groupby("theme")
    res = pd.DataFrame({"count": g.size(),
                        "severity": ((g["negativity"].mean() + g["severe"].mean()) / 2).round(3)})
    res["share_%"] = (res["count"] / len(work) * 100).round(1)
    res["priority"] = (res["share_%"] * res["severity"]).round(2)
    res["name"] = [kw(t) for t in res.index]
    res = res.sort_values("priority", ascending=False).reset_index()
    res.insert(0, "rank", range(1, len(res) + 1))
    prog.progress(100, text="Done!")
    st.success(f"✅ Analysed {len(work):,} complaints into {n_themes} themes.")
    for _, r in res.iterrows():
        st.markdown(f'<div class="problem"><span class="rank">#{int(r["rank"])}</span> '
                    f'<span class="name">{r["name"]}</span>'
                    f'<span class="badge b-vol">📈 {r["share_%"]}%</span>'
                    f'<span class="badge b-sev">⚠️ {sev_label(r["severity"])}</span>'
                    f'<span class="badge b-pri">🏆 {r["priority"]}</span></div>', unsafe_allow_html=True)
    st.download_button("⬇️ Download results (CSV)", res.to_csv(index=False).encode(),
                       "complaint_themes.csv", "text/csv")


# ===========================================================================
# CHAPTER 7 - TECH STACK  (owns: the technologies, as a reference)
# ===========================================================================
def page_tools():
    st.markdown('<div class="hero"><h1>🛠️ Chapter 7 — Tech Stack</h1>'
                '<p>A quick reference to every technology used. Chapter 4 explained the <i>concepts</i>; '
                'this lists the <i>tools</i> that implement them.</p></div>', unsafe_allow_html=True)
    chapter("This chapter owns: the tooling reference (what each piece of software is and why we chose it)")

    st.markdown("### 🧰 Foundations")
    tool("Python", "the programming language everything is written in.")
    tool("pandas", "works with data tables in code (like Excel). A table is called a 'DataFrame'.")
    tool("NumPy", "fast maths on arrays of numbers — used to store and slice the embedding vectors.")
    tool("Parquet", "a smart file format for tables — safe with messy free text, keeps data types, smaller than CSV. (CSV corrupted our dates once; Parquet fixed it.)")
    tool("Jupyter Notebook", "a document where code runs in small blocks with results shown right below — great for step-by-step work.")
    tool("Virtual environment (.venv)", "a private toolbox per project so library versions never clash between projects.")
    tool("Git & GitHub", "Git saves snapshots (commits) of the work; GitHub hosts them online so recruiters can see it.")

    st.markdown("### 🧠 NLP & Machine Learning")
    tool("sentence-transformers / all-MiniLM-L6-v2", "the pre-trained model that turns text into 384-number meaning-vectors (embeddings).")
    tool("scikit-learn — KMeans", "the clustering algorithm that groups the vectors into K themes.")
    tool("scikit-learn — TfidfVectorizer", "scores which words are distinctive to each theme (for keyword labels).")
    tool("scikit-learn — PCA", "shrinks 384 dimensions to 2 so the meaning-map can be drawn.")
    tool("VADER (vaderSentiment)", "a fast, transparent, dictionary-based sentiment tool — scores how negative a complaint is.")

    st.markdown("### 🤖 Generative AI & the App")
    tool("Google Gemini (google-genai)", "the LLM that reads each theme's keywords + examples and returns a clean human name.")
    tool("python-dotenv", "loads the secret API key from the hidden .env file so it's never hard-coded or pushed.")
    tool("Streamlit", "turns a Python script into this interactive web app — no HTML/CSS/JS needed.")
    tool("Plotly", "makes the interactive charts you can hover over and explore.")

    st.markdown("### 🔤 Glossary of key terms (all explained in Chapter 4)")
    st.markdown('<span class="pill">Embedding</span><span class="pill">Vector</span>'
                '<span class="pill">Clustering</span><span class="pill">Centroid</span>'
                '<span class="pill">Unsupervised learning</span><span class="pill">Sentiment</span>'
                '<span class="pill">TF-IDF</span><span class="pill">LLM / API key</span>'
                '<span class="pill">PCA</span><span class="pill">Priority matrix</span>'
                '<span class="pill">EDA</span><span class="pill">Reproducibility</span>', unsafe_allow_html=True)


# ===========================================================================
# CHAPTER 8 - DISCOVERIES & LEARNINGS  (owns: the honest engineering story)
# ===========================================================================
def page_learnings():
    st.markdown('<div class="hero"><h1>🎓 Chapter 8 — Discoveries & What I Learned</h1>'
                '<p>The honest engineering story — the bugs caught, the surprises, and the working habits. '
                'This is often what interviewers probe hardest.</p></div>', unsafe_allow_html=True)
    chapter("This chapter owns: the real problems hit and the lessons — not repeated anywhere else")

    step("🐞 The bug we caught — silently corrupted dates",
         "After extracting our slice, a 'complaints per month' chart looked flat and wrong. We didn't "
         "shrug it off. Investigating showed only ~6,281 of 124,962 dates were valid — the rest had "
         "silently become <b>NaT</b> (missing). Root cause: across an 8.5 GB CSV, pandas guessed the date "
         "column's type <i>differently in different chunks</i>, and joining them coerced most dates to "
         "missing. <b>Fix:</b> convert dates to a proper datetime <i>inside each chunk</i> before joining, "
         "and switch storage from CSV to Parquet (176 MB → 74 MB, and robust with commas/newlines in text). "
         "Result: 124,962/124,962 valid dates. <b>Lesson: never trust a result that looks off; sanity-check it.</b>")

    step("📈 The surprise — more data gave cleaner themes",
         "On the 18k sample, 'fraud' smeared messily across ~3 overlapping clusters. On the full 112k, those "
         "sub-types separated into distinct, sensible categories (Unauthorized Charges, Identity Theft, "
         "Unauthorized Applications, Account Closures). <b>Lesson: more data means KMeans centroids are "
         "estimated from more points, so groupings are less noisy and more stable.</b>")

    step("🧪 The habit — validate everything, with a reusable tool",
         "We built a reusable <code>validate()</code> function and ran it after <b>every</b> data step "
         "(size, nulls, duplicates, valid dates, sane labels). Validating <i>after</i> a transformation — "
         "not just before — is what caught the date bug. <b>Lesson: the biggest risk is assuming a step "
         "worked; always re-validate the output.</b>")

    step("🧯 The honesty — knowing the limits of my own work",
         "Severity is a <b>proxy</b> (lexicon sentiment + a hand-picked keyword list), not ground truth — "
         "VADER can misread sarcasm. KMeans needs K chosen up front and assumes round-ish clusters. Some "
         "themes still overlap. Stating these limits openly is a strength: it shows judgement, not just "
         "the ability to run an algorithm.")

    step("🔑 The engineering call — separate the slow step",
         "Embedding 112k complaints takes ~75 minutes. We ran it as its own script that <b>saves</b> the "
         "vectors, so an interruption in later analysis never wastes that expensive compute. Every "
         "downstream experiment reloads the saved vectors in seconds. Cheap step fast, expensive step once.")

    st.markdown("> **A great interview answer:** *“Tell me about a bug.”* → the date-corruption story above. "
                "It shows you profile data, question anomalies, find root causes, and fix them properly.")


# ===========================================================================
# CHAPTER 9 - NEXT & DEPLOY  (owns: automation + deployment)
# ===========================================================================
def page_future():
    st.markdown('<div class="hero"><h1>🚀 Chapter 9 — Automation, Deployment & Next</h1>'
                '<p>How this stops being a laptop project and becomes a tool a business can actually run — '
                'and how it reaches the world.</p></div>', unsafe_allow_html=True)
    chapter("This chapter owns: shipping — deployment, automation, and the roadmap")

    step("🖥️ On-demand today (this app)",
         "Anyone can open the <b>📤 Analyze Your File</b> tab, upload complaints, and get a ranked breakdown "
         "instantly — no code, no waiting for a data team. That's the headline deliverable, working now.")

    step("🌍 How it deploys (Streamlit Community Cloud, free)",
         "The app is pushed to GitHub, then connected to <b>Streamlit Community Cloud</b> — a free host that "
         "reads the repo, installs <code>requirements.txt</code>, and serves the app at a permanent public "
         "link, no install needed for visitors. The full 112k data stays local; a tiny "
         "<code>deploy_data.json</code> bundle (ranked themes + a few examples) is what the hosted app reads, "
         "so the repo stays light and the secret API key is never shipped.")

    step("⏰ Scheduled auto-refresh (planned)",
         "Using <b>GitHub Actions</b> (a free automation robot), the pipeline can run on a timer — pull the "
         "newest complaints, re-run embed → cluster → score → rank, and refresh a 'top new issues this week' "
         "report by itself. That's the 'runs itself' story: on-demand for humans, scheduled for the robot.")

    step("🧩 It generalizes anywhere",
         "The exact same pipeline works on any product or company's complaint/review text — point it at a "
         "different file and change one setting. Nothing about it is hard-wired to credit cards.")

    st.markdown("### 🧷 The GitHub workflow, in plain commands")
    st.markdown(
        "The save-and-ship cycle used throughout the project:")
    st.code(
        "git add <files>            # stage the files you want to save\n"
        "git commit -m \"message\"    # seal a save-point ON your computer\n"
        "git push                   # upload those commits to GitHub (the internet)\n\n"
        "# first time only, to connect a local repo to GitHub:\n"
        "git init\n"
        "git remote add origin https://github.com/<user>/<repo>.git\n"
        "git branch -M main\n"
        "git push -u origin main", language="bash")
    st.markdown("> **Key discipline:** big data files, the `.venv`, and the secret `.env` are listed in "
                "`.gitignore` so they are **never** uploaded. Repos hold code, not gigabytes or secrets.")


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.sidebar.markdown("## 🔍 Insight Engine")
st.sidebar.caption("Raw complaints → ranked problems to fix.")
PAGES = {
    "🏠 Home": page_home,
    "🎯 1 · The Problem": page_problem,
    "🗂️ 2 · The Data": page_data,
    "🧹 3 · Cleaning": page_cleaning,
    "🧠 4 · The AI Engine": page_engine,
    "📊 5 · The Results": page_results,
    "📤 6 · Analyze Your File": page_analyze,
    "🛠️ 7 · Tech Stack": page_tools,
    "🎓 8 · Discoveries": page_learnings,
    "🚀 9 · Next & Deploy": page_future,
}
choice = st.sidebar.radio("The story, in order:", list(PAGES.keys()))
st.sidebar.markdown("---")
st.sidebar.markdown("**The pipeline**\n\n🧠 Embeddings → 🧩 Clustering → 🔤 TF-IDF → ⚠️ Severity → 🏆 Priority → 🏷️ LLM naming")
st.sidebar.caption("Built on real CFPB open data · no fabrication.")

PAGES[choice]()
