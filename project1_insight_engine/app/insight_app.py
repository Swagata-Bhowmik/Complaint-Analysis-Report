# =============================================================================
# INSIGHT ENGINE - Streamlit storytelling dashboard (light olive theme)
# =============================================================================
# A rich, multi-section walkthrough of the whole project, explained simply,
# plus the live results and an upload analyzer.
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
# CSS — light olive/white, cards, badges, readable type.
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
.tool {background:#fff; border:1px solid #DDE7C4; border-left:5px solid #8FB04E; border-radius:10px;
       padding:12px 16px; margin-bottom:10px;}
.tool .n {font-weight:700; color:#556B2F;}
.tool .d {color:#4a552f; font-size:.94rem;}
.pill {display:inline-block; background:#EAF0D9; color:#556B2F; padding:4px 12px; border-radius:16px;
       font-size:.85rem; font-weight:600; margin:3px 4px 3px 0;}
h3 {margin-top:1.4rem !important; color:#3E4A22;}
blockquote {border-left:4px solid #6B8E23; background:#F2F5E9; padding:8px 16px; border-radius:6px; color:#3f4a2c;}
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

def tool(name, desc):
    st.markdown(f'<div class="tool"><span class="n">{name}</span> — <span class="d">{desc}</span></div>',
                unsafe_allow_html=True)


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
# PAGES
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

    st.markdown("### 👋 What is this, in one minute?")
    step("The idea",
         "Companies get thousands of complaints written in plain English. Nobody can read them all, "
         "so they never learn what's really wrong. This tool reads them <b>for</b> you and produces a "
         "clear, ranked list: <i>“here are the top problems, fix these first.”</i>")
    step("How to use this dashboard",
         "Use the sidebar to walk through the whole story: 🎯 the problem → 🗂️ the data → 🧹 cleaning → "
         "🧠 the AI engine → 📊 the results. Or jump to <b>📤 Analyze your file</b> to run it on your own "
         "complaints, and <b>🛠️ Tools</b> to understand every technology used, explained simply.")
    st.markdown("> **Golden rule of this project:** real public data only, no fabrication — every "
                "number here traces back to a real complaint and can be defended step by step.")


def page_problem():
    st.markdown('<div class="hero"><h1>🎯 The Problem & The Goal</h1>'
                '<p>Why this project exists and what success looks like.</p></div>', unsafe_allow_html=True)
    step("😖 The pain",
         "A bank (or any big company) receives <b>thousands of complaints every week</b> — about "
         "double charges, fraud, app failures, rude service. Reading them one-by-one is impossible, "
         "so the most valuable information — <i>what is actually going wrong</i> — stays buried. "
         "Managers end up guessing, or reacting only to whoever shouts loudest.")
    step("🎯 The goal",
         "Build a system that <b>automatically</b> answers three business questions: "
         "<br>1. What are people complaining about? (find the themes) "
         "<br>2. Which problems matter most? (rank by how common × how severe) "
         "<br>3. So what should we do? (a clear 'fix-first' list + a tool anyone can use).")
    step("💼 Why it matters (business value)",
         "Turning raw text into a ranked action plan means a company fixes the <b>right</b> things "
         "first — saving money, reducing churn, and improving customer trust. That's the difference "
         "between 'we ran an algorithm' and 'we answered a business question.'")
    st.markdown("> Interview one-liner: <i>“I built a system that turns raw customer complaints into a "
                "prioritized action plan — the top problems ranked by frequency and severity.”</i>")


def page_data():
    st.markdown('<div class="hero"><h1>🗂️ The Data</h1>'
                '<p>Real, public, and chosen carefully — the foundation of the whole project.</p></div>',
                unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    card(c1, "Source", "CFPB (US Govt)", small=True)
    card(c2, "Full size", "17M rows / 8.5 GB")
    card(c3, "Our scope", "112k credit-card", small=True)
    step("📚 What we used",
         "The <b>CFPB Consumer Complaint Database</b> — a free, public U.S. government dataset of real "
         "complaints about banks and credit cards. The key field is the <b>narrative</b>: the customer's "
         "own written story of what happened.")
    step("🧭 Why this data (and not scraping app reviews)",
         "We deliberately chose authoritative open data over scraping Play Store / app reviews. "
         "Scraping is against platform terms, unreliable (blocks, only a few reviews), and raises "
         "privacy issues. <b>“Publicly visible” is not the same as “free & safe to bulk-collect.”</b> "
         "CFPB is legal, large, and defensible — a stronger interview story.")
    step("🔬 What profiling the data taught us (EDA)",
         "Before building anything we explored the whole 8.5 GB file (in memory-safe chunks): "
         "<ul><li>Narratives only exist from <b>2015 onward</b> (opt-in) — the oldest rows look empty.</li>"
         "<li>The same product had <b>multiple different labels</b> over the years.</li>"
         "<li>We caught a <b>silent bug</b>: dates got corrupted during extraction. A chart looked wrong, "
         "we investigated, and fixed it — proof you must sanity-check everything.</li></ul>")
    st.markdown("> Lesson: <i>“Understand your data before you touch it. If the data is wrong, "
                "everything built on it is wrong.”</i>")


def page_cleaning():
    st.markdown('<div class="hero"><h1>🧹 Cleaning the Text</h1>'
                '<p>Careful cleaning that removes noise without destroying meaning.</p></div>',
                unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    card(c1, "Before", "124,962")
    card(c2, "Removed", "12,481", small=False)
    card(c3, "After (clean)", "112,481")
    step("🧯 The problems we found",
         "<ul><li><b>~12,000 duplicate</b> complaints (same text repeated) — they lie about how common "
         "a problem is.</li><li>Privacy masks everywhere: <code>XXXX</code> (names), "
         "<code>XX/XX/year&gt;</code> (dates), <code>{$70.00}</code> (money).</li>"
         "<li>Two names for the same product.</li></ul>")
    step("🧼 What we did (carefully)",
         "Removed duplicates, merged the product labels, and turned the privacy masks into neat "
         "placeholders (<code>&lt;redacted&gt;</code>, <code>&lt;date&gt;</code>, <code>&lt;money&gt;</code>) "
         "instead of deleting them — so the real sentence stays readable but the noise is gone. "
         "We kept the original text too, so we can always show before/after.")
    st.markdown("**Real before → after example:**")
    st.markdown('<blockquote><b>Before:</b> “In XX/XX/year&gt;, XXXX applied charges higher than I agreed…”'
                '<br><b>After:</b> “In &lt;date&gt;, &lt;redacted&gt; applied charges higher than I agreed…”'
                '</blockquote>', unsafe_allow_html=True)
    st.markdown("> Lesson: <i>over-cleaning destroys signal. Clean just enough to remove noise, and "
                "always keep the raw text for auditability.</i>")


def page_engine():
    st.markdown('<div class="hero"><h1>🧠 The AI Engine</h1>'
                '<p>How the computer actually “reads” complaints and finds the problems — in 5 steps.</p></div>',
                unsafe_allow_html=True)
    step("🧠 Step 1 — Embeddings (give each complaint a location on a “meaning-map”)",
         "Computers understand numbers, not words. So each complaint is turned into a list of "
         "<b>384 numbers</b> (a 'vector') that captures its <b>meaning</b>. Complaints that mean similar "
         "things get similar numbers, so they sit close together on an imaginary map. "
         "Tool: <b>sentence-transformers</b>, model <b>all-MiniLM-L6-v2</b>.")
    step("🧩 Step 2 — Clustering (circle the crowds on the map)",
         "Now every complaint is a dot on the meaning-map. <b>Clustering</b> finds the crowds of dots — "
         "each crowd is a group of similar complaints = a <b>theme</b>. Algorithm: <b>KMeans</b> "
         "(you say 'make 12 groups'; it finds the 12 natural centers and assigns each complaint to the "
         "nearest one).")
    step("⚠️ Step 3 — Severity (how bad is each problem?)",
         "Volume isn't enough — a business cares how <b>serious</b> a problem is. We score each complaint's "
         "negativity with <b>VADER</b> (a sentiment tool) and flag high-stakes words (fraud, stolen, "
         "identity theft). Averaged per theme = a severity score.")
    step("🏆 Step 4 — Priority (the smart ranking)",
         "<b>Priority = Volume × Severity.</b> This surfaces problems that are both common AND serious — "
         "not just a popularity contest. It's the classic business 'priority matrix' idea.")
    step("🏷️ Step 5 — AI naming (give each theme a human name)",
         "The groups start as 'Theme 0, 1, 2…'. We send each theme's keywords + example complaints to an "
         "<b>LLM (Google Gemini)</b> and ask for a short, clear name and description — e.g. "
         "'Unauthorized / Fraudulent Charges'.")
    st.markdown("**Helper techniques:** ")
    st.markdown('<span class="pill">TF-IDF → find each theme\'s distinctive keywords</span>'
                '<span class="pill">PCA → squash 384 numbers to 2 for plotting</span>'
                '<span class="pill">Caching → embed once, reuse forever</span>', unsafe_allow_html=True)


def page_results():
    st.markdown('<div class="hero"><h1>📊 The Results</h1>'
                '<p>The top credit-card problems, discovered automatically from 112,481 complaints.</p></div>',
                unsafe_allow_html=True)
    themes, total, examples = load_full_results()
    st.markdown("### 📈 Visualize")
    style = st.radio("Chart style:", ["Ranked bars", "Treemap (boxes)", "Priority matrix"], horizontal=True)
    if style == "Ranked bars":
        st.caption("Longer bar = higher priority (common × severe). Colour = severity.")
        st.plotly_chart(chart_ranked_bars(themes), use_container_width=True)
    elif style.startswith("Treemap"):
        st.caption("Box size = number of complaints. Darker green = more severe.")
        st.plotly_chart(chart_treemap(themes), use_container_width=True)
    else:
        st.caption("Bubbles numbered by rank. Right = common, Up = severe. Hover for detail.")
        st.plotly_chart(chart_matrix(themes), use_container_width=True)

    st.markdown("### 🏆 Ranked problems")
    for _, r in themes.iterrows():
        st.markdown(f'<div class="problem"><span class="rank">#{int(r["rank"])}</span> '
                    f'<span class="name">{r["name"]}</span><div class="desc">{r["description"]}</div>'
                    f'<span class="badge b-vol">📈 {r["share_%"]}% of complaints</span>'
                    f'<span class="badge b-sev">⚠️ Severity: {sev_label(r["severity"])} ({r["severity"]})</span>'
                    f'<span class="badge b-pri">🏆 Priority {r["priority"]}</span></div>', unsafe_allow_html=True)

    st.markdown("### 🔎 Read real complaints behind a theme")
    pick = st.selectbox("Choose a theme:", themes["name"].tolist())
    tid = int(themes[themes["name"] == pick].iloc[0]["theme"])
    for i, e in enumerate(examples.get(tid, []), 1):
        with st.expander(f"Example {i}"):
            st.write(str(e) + "…")


def page_analyze():
    st.markdown('<div class="hero"><h1>📤 Analyze Your Own Complaints</h1>'
                '<p>Upload a CSV/Excel of complaints → get an instant ranked breakdown. '
                '(Free demo analyses up to 1,500 rows.)</p></div>', unsafe_allow_html=True)
    up = st.file_uploader("Upload complaints file (CSV or Excel)", type=["csv", "xlsx"])
    if up is None:
        st.info("👆 Upload a file with a column of complaint text to begin.")
        return
    df = pd.read_csv(up) if up.name.endswith(".csv") else pd.read_excel(up)
    st.success(f"✅ Loaded {len(df):,} rows.")
    col = st.selectbox("Which column has the complaint text?", df.columns.tolist())
    n_themes = st.slider("How many themes to find?", 3, 12, 6)
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


def page_tools():
    st.markdown('<div class="hero"><h1>🛠️ Tools & Tech — explained simply</h1>'
                '<p>Every technology used in this project, in plain words.</p></div>', unsafe_allow_html=True)
    st.markdown("### 🧰 Foundations")
    tool("Python", "the programming language everything is written in.")
    tool("pandas", "works with data tables in code (like Excel). A table is a 'DataFrame'.")
    tool("Parquet", "a smart file format for tables — safe with messy text, keeps data types, smaller than CSV.")
    tool("Virtual environment (.venv)", "a private toolbox per project so libraries never clash.")
    tool("Git & GitHub", "Git saves snapshots of the work; GitHub hosts them online for others to see.")
    st.markdown("### 🧠 NLP & Machine Learning")
    tool("sentence-transformers / all-MiniLM-L6-v2", "the AI model that turns text into 384-number 'meaning-vectors' (embeddings).")
    tool("Embeddings", "numeric fingerprints of meaning — similar texts get similar numbers.")
    tool("KMeans (scikit-learn)", "clustering algorithm that groups the vectors into K themes.")
    tool("TF-IDF", "scores which words are special to one group — used to label themes with keywords.")
    tool("PCA", "shrinks 384 dimensions to 2 so we can draw the meaning-map on a flat chart.")
    tool("VADER", "a fast sentiment tool that scores how negative/positive a text is.")
    st.markdown("### 🤖 Generative AI & App")
    tool("Google Gemini (LLM)", "a large language model that reads each theme and gives it a clear human name.")
    tool("Streamlit", "turns Python into an interactive web app (this dashboard) with no web-design needed.")
    tool("Plotly", "makes the interactive charts you can hover and explore.")
    st.markdown("### 🔤 Key terms")
    st.markdown('<span class="pill">Embedding</span><span class="pill">Vector</span>'
                '<span class="pill">Clustering</span><span class="pill">Centroid</span>'
                '<span class="pill">Sentiment</span><span class="pill">TF-IDF</span>'
                '<span class="pill">LLM</span><span class="pill">Priority matrix</span>'
                '<span class="pill">EDA</span><span class="pill">Reproducibility</span>', unsafe_allow_html=True)


def page_learnings():
    st.markdown('<div class="hero"><h1>🎓 Discoveries & What I Learned</h1>'
                '<p>The honest lessons — great for interviews.</p></div>', unsafe_allow_html=True)
    step("🐞 Discovery — trust nothing unverified",
         "A time chart looked flat/wrong. Investigating revealed our dates had been <b>silently "
         "corrupted</b> during extraction (a data-type mix-up when joining chunks). We fixed it and "
         "switched to Parquet. <b>Lesson: always sanity-check a result that looks off.</b>")
    step("📈 Discovery — more data, cleaner themes",
         "On a small 18k sample, 'fraud' spread messily across several overlapping clusters. On the full "
         "112k, the themes separated cleanly into distinct categories. <b>Lesson: more data reduces "
         "clustering noise.</b>")
    step("🥇 Discovery — fraud dominates",
         "The #1 problem — unauthorized/fraudulent charges — is both the <b>most common (13.4%) and the "
         "most severe</b>. Disputes and credit-reporting issues follow. A clear, actionable headline.")
    step("🧪 Habit — validate everything",
         "We validated after <b>every</b> step (completeness, duplicates, valid dates, sane labels) using "
         "a reusable check — and showed real before/after examples, never just summary numbers.")
    step("💬 Interview-ready answers",
         "<ul><li><b>Why CFPB not scraping?</b> Legal, large, defensible; scraping breaks terms and is "
         "unreliable.</li><li><b>How did you find themes without labels?</b> Unsupervised learning: "
         "embeddings + KMeans, labelled with TF-IDF + an LLM.</li><li><b>How did you prioritize?</b> "
         "volume × severity, shown as a priority matrix.</li></ul>")


def page_future():
    st.markdown('<div class="hero"><h1>🚀 Automation & What\'s Next</h1>'
                '<p>How this becomes a self-running tool a business can actually use.</p></div>',
                unsafe_allow_html=True)
    step("🔄 On-demand (this app)",
         "Anyone can upload a complaints file and get the analysis instantly — no code, no waiting for "
         "a data team.")
    step("⏰ Scheduled auto-refresh (planned)",
         "Using <b>GitHub Actions</b> (a free automation robot), the pipeline can run on a timer — pull "
         "the newest complaints, re-analyze, and refresh a 'top new issues this week' report by itself.")
    step("🌍 Public deployment (planned)",
         "Deploy this app to <b>Streamlit Community Cloud</b> (free) so it has a permanent public link "
         "anyone can open — no install required.")
    step("🧩 Generalizes anywhere",
         "The same pipeline works on any product or company's complaint/review text — just point it at a "
         "different file. Change one setting and it re-scopes.")


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.sidebar.markdown("## 🔍 Insight Engine")
st.sidebar.caption("Raw complaints → ranked problems to fix.")
PAGES = {
    "🏠 Home": page_home,
    "🎯 The Problem": page_problem,
    "🗂️ The Data": page_data,
    "🧹 Cleaning": page_cleaning,
    "🧠 The AI Engine": page_engine,
    "📊 Results": page_results,
    "📤 Analyze your file": page_analyze,
    "🛠️ Tools & Tech": page_tools,
    "🎓 Discoveries & Learnings": page_learnings,
    "🚀 Automation & Next": page_future,
}
choice = st.sidebar.radio("Navigate the story:", list(PAGES.keys()))
st.sidebar.markdown("---")
st.sidebar.markdown("**Pipeline**\n\n🧠 Embeddings → 🧩 Clustering → ⚠️ Severity → 🏆 Priority → 🏷️ AI naming")
st.sidebar.caption("Built on real CFPB open data · no fabrication.")

PAGES[choice]()
