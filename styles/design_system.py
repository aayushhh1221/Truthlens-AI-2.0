"""
TruthLens AI — Design System CSS
Clean, professional, enterprise-grade.
"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@600;700;800;900&display=swap');

/* ══════════════════════════════════════════
   ROOT VARIABLES
══════════════════════════════════════════ */
:root {
    --bg:       #050B26;
    --bg2:      #07102E;
    --card:     #0D1736;
    --card2:    #111A3D;
    --p:        #7C4DFF;
    --p-light:  #A67AFF;
    --p-dark:   #5533CC;
    --p-glow:   rgba(124,77,255,0.28);
    --s:        #00CFFF;
    --s-glow:   rgba(0,207,255,0.22);
    --green:    #00E5A0;
    --yellow:   #FFB800;
    --red:      #FF4560;
    --tx:       #FFFFFF;
    --tx-m:     #B0BAD6;
    --tx-d:     #5B6A9A;
    --border:   rgba(124,77,255,0.16);
    --border-s: rgba(255,255,255,0.07);
    --r:        12px;
    --r-sm:     8px;
    --r-lg:     16px;
    --shadow:   0 8px 32px rgba(0,0,0,0.55);
    --font:     'Inter', sans-serif;
    --font-d:   'Poppins', sans-serif;
}

/* ══════════════════════════════════════════
   BACKGROUND TRANSPARENCY RESET
   Fixes all Streamlit container color bleed
══════════════════════════════════════════ */
.stApp,
.stApp > .main,
.main,
section.main,
.block-container,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMainBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stElementContainer"],
[data-testid="column"],
div[class*="stColumn"],
div[class*="css-"],
.element-container,
.stMarkdown {
    background: transparent !important;
    background-color: transparent !important;
}

/* App root gets the actual background */
.stApp {
    background-color: var(--bg) !important;
    background-image:
        radial-gradient(ellipse 70% 55% at 12% 4%, rgba(124,77,255,0.13) 0%, transparent 52%),
        radial-gradient(ellipse 55% 45% at 88% 96%, rgba(0,207,255,0.08) 0%, transparent 52%),
        radial-gradient(circle at 1px 1px, rgba(255,255,255,0.030) 1px, transparent 0) !important;
    background-size: 100% 100%, 100% 100%, 32px 32px !important;
    background-attachment: fixed !important;
    font-family: var(--font) !important;
    color: var(--tx) !important;
}

/* Hide Streamlit chrome completely */
#MainMenu, footer,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stDeployButton"],
.stDeployButton,
[data-testid="stSidebar"] { display: none !important; }

.block-container {
    max-width: 1200px !important;
    padding: 0 28px 80px !important;
    margin: 0 auto !important;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--p); border-radius: 2px; }

/* ══════════════════════════════════════════
   NAVBAR
══════════════════════════════════════════ */
[data-testid="stHorizontalBlock"]:has(.nav-marker) {
    background: rgba(5,11,38,0.88) !important;
    backdrop-filter: blur(28px) !important;
    -webkit-backdrop-filter: blur(28px) !important;
    border-bottom: 1px solid rgba(124,77,255,0.14) !important;
    padding: 0 28px !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 900 !important;
    margin: 0 -28px !important;
    border-radius: 0 !important;
    gap: 0 !important;
    align-items: center !important;
    min-height: 60px !important;
}

/* Kill ALL child backgrounds inside navbar row */
[data-testid="stHorizontalBlock"]:has(.nav-marker) > *,
[data-testid="stHorizontalBlock"]:has(.nav-marker) > * > *,
[data-testid="stHorizontalBlock"]:has(.nav-marker) [data-testid="column"],
[data-testid="stHorizontalBlock"]:has(.nav-marker) [data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"]:has(.nav-marker) [data-testid="stElementContainer"],
[data-testid="stHorizontalBlock"]:has(.nav-marker) .stMarkdown {
    background: transparent !important;
    background-color: transparent !important;
}

.nav-brand {
    display: flex; align-items: center; gap: 10px;
    height: 60px;
}
.nav-brand-logo {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, var(--p), var(--s));
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem; font-weight: 800; color: white;
    flex-shrink: 0;
}
.nav-brand-text {
    font-family: var(--font-d);
    font-size: 1.05rem; font-weight: 800;
    background: linear-gradient(135deg, var(--p-light) 0%, var(--s) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    white-space: nowrap; letter-spacing: -0.01em;
}

[data-testid="stHorizontalBlock"]:has(.nav-marker) .stButton > button {
    background: transparent !important;
    color: var(--tx-m) !important;
    border: none !important;
    border-radius: var(--r-sm) !important;
    font-family: var(--font) !important;
    font-size: 0.87rem !important;
    font-weight: 500 !important;
    padding: 7px 12px !important;
    height: 36px !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
    letter-spacing: 0.01em !important;
    min-width: 150px !important;
    white-space: nowrap !important;
}
[data-testid="stHorizontalBlock"]:has(.nav-marker) .stButton > button:hover {
    color: var(--tx) !important;
    background: rgba(124,77,255,0.10) !important;
    transform: none !important;
    box-shadow: none !important;
}
.nav-active-item {
    display: flex; align-items: center; justify-content: center;
    height: 36px;
    font-size: 0.87rem; font-weight: 600;
    color: var(--p-light);
    background: rgba(124,77,255,0.12);
    border: 1px solid rgba(124,77,255,0.25);
    border-radius: var(--r-sm);
    padding: 0 12px;
    white-space: nowrap; letter-spacing: 0.01em;
}

/* ══════════════════════════════════════════
   GLOBAL BUTTONS (non-navbar)
══════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, var(--p), var(--p-dark)) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--r-sm) !important;
    font-family: var(--font) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 10px 22px !important;
    transition: all 0.22s ease !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 2px 12px var(--p-glow) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px var(--p-glow) !important;
    opacity: 0.92 !important;
}

/* ══════════════════════════════════════════
   INPUTS
══════════════════════════════════════════ */
.stTextArea textarea, .stTextInput input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    color: var(--tx) !important;
    font-family: var(--font) !important;
    font-size: 0.9rem !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--p) !important;
    box-shadow: 0 0 0 3px var(--p-glow) !important;
    outline: none !important;
}
.stTextArea label, .stTextInput label, .stSelectbox label,
.stFileUploader label { color: var(--tx-m) !important; }
.stSelectbox > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--tx) !important;
    border-radius: var(--r-sm) !important;
}

/* ══════════════════════════════════════════
   TABS
══════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border-s) !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--tx-m) !important;
    border: none !important;
    border-radius: var(--r-sm) var(--r-sm) 0 0 !important;
    font-family: var(--font) !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 10px 18px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(124,77,255,0.10) !important;
    color: var(--p-light) !important;
    border-bottom: 2px solid var(--p) !important;
}

/* ══════════════════════════════════════════
   METRICS / PROGRESS / UPLOADER
══════════════════════════════════════════ */
div[data-testid="metric-container"] {
    background: var(--card) !important;
    border: 1px solid var(--border-s) !important;
    border-radius: var(--r) !important;
    padding: 18px !important;
}
div[data-testid="metric-container"] label {
    color: var(--tx-m) !important; font-size: 0.76rem !important;
    text-transform: uppercase !important; letter-spacing: 0.08em !important;
}
.stProgress > div > div {
    background: linear-gradient(90deg, var(--p), var(--s)) !important;
    border-radius: 100px !important;
}
.stFileUploader {
    border: 1.5px dashed var(--border) !important;
    border-radius: var(--r) !important;
    background: rgba(124,77,255,0.03) !important;
}

/* ══════════════════════════════════════════
   TYPOGRAPHY HELPERS
══════════════════════════════════════════ */
.section-label {
    font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--p-light); margin-bottom: 10px;
}
.section-title {
    font-family: var(--font-d);
    font-size: clamp(1.75rem, 3.5vw, 2.4rem);
    font-weight: 800; color: var(--tx);
    line-height: 1.1; margin-bottom: 14px;
}
.section-subtitle {
    font-size: 0.96rem; color: var(--tx-m);
    line-height: 1.65; max-width: 540px; margin: 0 auto;
}
.grad-text {
    background: linear-gradient(135deg, var(--p-light) 0%, var(--s) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.section-divider {
    border: none; height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 60px 0;
}

/* ══════════════════════════════════════════
   HERO
══════════════════════════════════════════ */
.hero-wrap {
    padding: 72px 0 56px; text-align: center;
}
.hero-eyebrow {
    display: inline-block;
    background: rgba(124,77,255,0.12);
    border: 1px solid rgba(124,77,255,0.28);
    color: var(--p-light);
    padding: 5px 16px; border-radius: 100px;
    font-size: 0.76rem; font-weight: 600;
    letter-spacing: 0.09em; text-transform: uppercase;
    margin-bottom: 22px;
}
.hero-title {
    font-family: var(--font-d);
    font-size: clamp(3rem, 5.5vw, 4.8rem);
    font-weight: 800;
    line-height: 0.95;
    margin: 0 0 20px;
    background: linear-gradient(140deg, #FFFFFF 20%, var(--p-light) 55%, var(--s) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-desc {
    font-size: clamp(1rem, 2vw, 1.15rem);
    color: var(--tx-m);
    max-width: 800px;
    margin: 0 auto 34px;
    line-height: 1.8;
    text-align: center;
}
.hero-cta { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-bottom: 52px; }
.btn-hero-primary {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 13px 28px;
    background: linear-gradient(135deg, var(--p), var(--p-dark));
    color: white; border: none; border-radius: var(--r-sm);
    font-family: var(--font); font-weight: 600; font-size: 0.9rem;
    cursor: pointer; text-decoration: none; transition: all 0.22s;
    box-shadow: 0 3px 16px var(--p-glow); letter-spacing: 0.02em;
}
.btn-hero-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 28px var(--p-glow); }
.btn-hero-outline {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 13px 28px; background: transparent; color: var(--tx);
    border: 1.5px solid rgba(124,77,255,0.35); border-radius: var(--r-sm);
    font-family: var(--font); font-weight: 600; font-size: 0.9rem;
    cursor: pointer; text-decoration: none; transition: all 0.22s; letter-spacing: 0.02em;
}
.btn-hero-outline:hover { background: rgba(124,77,255,0.10); border-color: var(--p); }

.hero-stats {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 12px; max-width: 820px; margin: 0 auto;
}
.hero-stat {
    background: rgba(13,23,54,0.75);
    border: 1px solid var(--border); border-radius: var(--r);
    padding: 18px 14px; text-align: center;
    backdrop-filter: blur(12px); transition: all 0.3s;
}
.hero-stat:hover { transform: translateY(-3px); box-shadow: 0 8px 28px rgba(124,77,255,0.18); }
.hero-stat-val {
    font-family: var(--font-d); font-size: 1.85rem; font-weight: 800;
    background: linear-gradient(135deg, var(--p-light), var(--s));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    line-height: 1; margin-bottom: 6px;
}
.hero-stat-lbl { font-size: 0.73rem; color: var(--tx-m); font-weight: 500; text-transform: uppercase; letter-spacing: 0.07em; }

/* ══════════════════════════════════════════
   PROBLEM CARDS
══════════════════════════════════════════ */
.problem-card {
    background: var(--card); border: 1px solid var(--border-s);
    border-radius: var(--r); padding: 26px 22px;
    transition: all 0.3s; height: 100%;
}
.problem-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(0,0,0,0.5); }
.prob-tag {
    display: inline-block; font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.11em; text-transform: uppercase;
    padding: 3px 10px; border-radius: 4px; margin-bottom: 14px;
}
.prob-tag-red    { color: var(--red);    background: rgba(255,69,96,0.12);  }
.prob-tag-yellow { color: var(--yellow); background: rgba(255,184,0,0.12);  }
.prob-tag-purple { color: var(--p-light);background: rgba(124,77,255,0.12); }
.prob-tag-cyan   { color: var(--s);      background: rgba(0,207,255,0.10);  }
.prob-stat { font-family: var(--font-d); font-size: 2.1rem; font-weight: 800; margin-top: 14px; line-height: 1; }
.prob-stat-red    { color: var(--red); }
.prob-stat-yellow { color: var(--yellow); }
.prob-stat-purple { color: var(--p-light); }
.prob-stat-cyan   { color: var(--s); }
.prob-title { font-size: 0.96rem; font-weight: 700; color: var(--tx); margin-bottom: 6px; }
.prob-desc  { font-size: 0.82rem; color: var(--tx-m); line-height: 1.55; }

.why-matters {
    background: rgba(124,77,255,0.06);
    border: 1px solid rgba(124,77,255,0.18); border-radius: var(--r);
    padding: 18px 24px; display: flex; align-items: center;
    justify-content: space-between; flex-wrap: wrap; gap: 14px; margin-top: 18px;
}
.why-matters-title { font-weight: 700; font-size: 0.93rem; color: var(--tx); margin-bottom: 3px; }
.why-matters-desc  { font-size: 0.82rem; color: var(--tx-m); max-width: 420px; line-height: 1.5; }
.why-matters-tags  { display: flex; gap: 14px; flex-wrap: wrap; }
.wm-tag { font-size: 0.84rem; font-weight: 700; }
.wm-tag-cyan   { color: var(--s); }
.wm-tag-purple { color: var(--p-light); }
.wm-tag-green  { color: var(--green); }

/* ══════════════════════════════════════════
   HOW IT WORKS — PROFESSIONAL STEP CARDS
   No emojis. Number-driven, clean typography.
══════════════════════════════════════════ */
.step-card {
    background: var(--card); border: 1px solid var(--border-s);
    border-radius: var(--r); padding: 28px 22px 24px;
    transition: all 0.3s; position: relative; overflow: hidden;
}
.step-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--p), var(--s));
}
.step-card:hover { transform: translateY(-4px); box-shadow: var(--shadow); border-color: rgba(124,77,255,0.25); }
.step-num-badge {
    font-family: var(--font-d);
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--p-light); margin-bottom: 16px;
    background: rgba(124,77,255,0.1);
    border: 1px solid rgba(124,77,255,0.22);
    display: inline-block; padding: 3px 10px; border-radius: 4px;
}
.step-title { font-family: var(--font-d); font-size: 0.98rem; font-weight: 700; color: var(--tx); margin-bottom: 10px; }
.step-desc  { font-size: 0.82rem; color: var(--tx-m); line-height: 1.6; }

/* ══════════════════════════════════════════
   FEATURE CARDS (Core Tech)
══════════════════════════════════════════ */
.feature-card {
    background: var(--card); border: 1px solid var(--border-s);
    border-radius: var(--r-lg); padding: 30px 28px;
    height: 100%; transition: all 0.3s; position: relative; overflow: hidden;
}
.feature-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--p), var(--s));
}
.feature-card:hover { border-color: rgba(124,77,255,0.28); box-shadow: 0 12px 44px rgba(124,77,255,0.12); transform: translateY(-4px); }
.fc-label {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--p-light);
    background: rgba(124,77,255,0.1); border: 1px solid rgba(124,77,255,0.2);
    padding: 4px 10px; border-radius: 4px; display: inline-block; margin-bottom: 18px;
}
.fc-title { font-family: var(--font-d); font-size: 1.3rem; font-weight: 700; color: var(--tx); margin-bottom: 8px; }
.fc-sub   { font-size: 0.84rem; color: var(--tx-m); margin-bottom: 20px; line-height: 1.58; }
.fc-list  { list-style: none; padding: 0; margin: 0 0 22px; }
.fc-item  {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 0; border-bottom: 1px solid var(--border-s);
    font-size: 0.86rem; color: var(--tx-m);
}
.fc-item:last-child { border-bottom: none; }
.fc-check {
    width: 18px; height: 18px; background: rgba(0,229,160,0.12);
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 0.7rem; color: var(--green); flex-shrink: 0;
}
.integration-bar {
    background: rgba(124,77,255,0.07); border: 1px solid rgba(124,77,255,0.18);
    border-radius: var(--r); padding: 14px 22px;
    display: flex; align-items: center; justify-content: space-between; gap: 12px;
    margin-top: 14px; flex-wrap: wrap;
}
.ib-left  { display: flex; align-items: center; gap: 10px; }
.ib-title { font-weight: 700; font-size: 0.88rem; color: var(--tx); }
.ib-desc  { font-size: 0.78rem; color: var(--tx-m); }
.ib-link  { font-size: 0.8rem; color: var(--p-light); font-weight: 600; cursor: pointer; white-space: nowrap; }

/* ══════════════════════════════════════════
   KPI CARDS
══════════════════════════════════════════ */
.kpi-card {
    background: var(--card); border: 1px solid var(--border-s);
    border-radius: var(--r); padding: 28px 18px; text-align: center; transition: all 0.3s;
}
.kpi-card:hover { border-color: var(--border); transform: translateY(-3px); box-shadow: 0 10px 36px rgba(124,77,255,0.12); }
.kpi-val {
    font-family: var(--font-d); font-size: clamp(1.9rem, 3.5vw, 2.7rem); font-weight: 900;
    background: linear-gradient(135deg, var(--p-light), var(--s));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    line-height: 1; margin-bottom: 8px;
}
.kpi-lbl { font-size: 0.82rem; color: var(--tx-m); font-weight: 500; letter-spacing: 0.03em; }

/* ══════════════════════════════════════════
   WHY CARDS — Professional, no emojis
══════════════════════════════════════════ */
.why-card {
    background: var(--card); border: 1px solid var(--border-s);
    border-radius: var(--r); padding: 22px 20px; transition: all 0.3s; height: 100%;
}
.why-card:hover { border-color: var(--border); transform: translateY(-3px); box-shadow: 0 8px 32px rgba(124,77,255,0.11); }
.wc-index {
    font-family: var(--font-d); font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--p-light); margin-bottom: 12px;
    background: rgba(124,77,255,0.1); border: 1px solid rgba(124,77,255,0.2);
    display: inline-block; padding: 3px 8px; border-radius: 4px;
}
.wc-title { font-weight: 700; font-size: 0.93rem; color: var(--tx); margin-bottom: 7px; }
.wc-desc  { font-size: 0.81rem; color: var(--tx-m); line-height: 1.58; }

/* ══════════════════════════════════════════
   TEAM CARDS — Enterprise glassmorphism
   No gradients. Clean, professional.
══════════════════════════════════════════ */
.team-section-title {
    font-family: var(--font-d);
    font-size: clamp(1.8rem, 4vw, 2.4rem); font-weight: 800;
    color: var(--tx); text-align: center; margin-bottom: 10px;
}
.team-section-sub {
    text-align: center; color: var(--tx-m); font-size: 0.93rem;
    margin-bottom: 36px; line-height: 1.6;
}
.team-card {
    background: var(--card);
    border: 1px solid var(--border-s);
    border-radius: var(--r-lg);
    padding: 26px 22px;
    transition: all 0.3s; height: 100%;
    position: relative; overflow: hidden;
}
.team-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--p), var(--s));
}
.team-card:hover {
    border-color: rgba(124,77,255,0.28);
    transform: translateY(-5px);
    box-shadow: 0 14px 44px rgba(0,0,0,0.45), 0 0 0 1px rgba(124,77,255,0.2);
}
.tc-header   { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }
.tc-avatar {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, rgba(124,77,255,0.25), rgba(0,207,255,0.15));
    border: 1.5px solid rgba(124,77,255,0.3);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-d); font-size: 1.1rem; font-weight: 700; color: var(--p-light);
}
.tc-social { display: flex; gap: 6px; padding-top: 2px; }
.tc-social-link {
    width: 26px; height: 26px;
    background: rgba(255,255,255,0.05); border: 1px solid var(--border-s);
    border-radius: 6px; display: flex; align-items: center; justify-content: center;
    font-size: 0.68rem; font-weight: 700; color: var(--tx-m);
    text-decoration: none; transition: all 0.2s;
}
.tc-social-link:hover { background: rgba(124,77,255,0.15); color: var(--p-light); border-color: var(--border); }
.tc-name  { font-family: var(--font-d); font-size: 0.98rem; font-weight: 700; color: var(--tx); margin-bottom: 3px; }
.tc-role  { font-size: 0.76rem; color: var(--p-light); font-weight: 600; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 12px; }
.tc-resp-title { font-size: 0.72rem; font-weight: 600; color: var(--tx-d); text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 6px; }
.tc-resp-list { list-style: none; padding: 0; margin: 0 0 14px; }
.tc-resp-item {
    font-size: 0.81rem; color: var(--tx-m); padding: 4px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    display: flex; align-items: center; gap: 7px;
}
.tc-resp-item:last-child { border-bottom: none; }
.tc-resp-dot { width: 4px; height: 4px; border-radius: 50%; background: var(--p); flex-shrink: 0; }
.tc-badge-row { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 12px; }
.tc-badge {
    font-size: 0.7rem; font-weight: 600;
    padding: 3px 9px; border-radius: 4px;
    background: rgba(124,77,255,0.1); border: 1px solid rgba(124,77,255,0.2);
    color: var(--p-light); letter-spacing: 0.04em;
}
.tc-badge-lead {
    background: rgba(255,184,0,0.1); border: 1px solid rgba(255,184,0,0.25);
    color: var(--yellow);
}

/* ══════════════════════════════════════════
   GLASS CARD (generic)
══════════════════════════════════════════ */
.glass-card {
    background: var(--card); border: 1px solid var(--border-s);
    border-radius: var(--r); padding: 22px; transition: all 0.3s;
}
.glass-card:hover { border-color: var(--border); box-shadow: var(--shadow); }

/* ══════════════════════════════════════════
   DETECTION RESULT COMPONENTS
══════════════════════════════════════════ */
.verdict-fake {
    background: rgba(255,69,96,0.09); border: 1.5px solid rgba(255,69,96,0.35);
    border-radius: var(--r); padding: 18px 22px;
    display: flex; align-items: center; gap: 14px;
    font-family: var(--font-d); font-size: 1.1rem; font-weight: 700; color: #FF8090;
}
.verdict-real {
    background: rgba(0,229,160,0.09); border: 1.5px solid rgba(0,229,160,0.35);
    border-radius: var(--r); padding: 18px 22px;
    display: flex; align-items: center; gap: 14px;
    font-family: var(--font-d); font-size: 1.1rem; font-weight: 700; color: var(--green);
}
.verdict-uncertain {
    background: rgba(255,184,0,0.09); border: 1.5px solid rgba(255,184,0,0.35);
    border-radius: var(--r); padding: 18px 22px;
    display: flex; align-items: center; gap: 14px;
    font-family: var(--font-d); font-size: 1.1rem; font-weight: 700; color: var(--yellow);
}
.verdict-icon { font-size: 1.8rem; flex-shrink: 0; }
.verdict-sub  { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.1em; opacity: 0.6; margin-bottom: 3px; text-transform: uppercase; }

.score-bar-wrap { margin-bottom: 13px; }
.score-bar-hdr  { display: flex; justify-content: space-between; margin-bottom: 5px; }
.score-bar-lbl  { font-size: 0.83rem; color: var(--tx-m); font-weight: 500; }
.score-bar-num  { font-size: 0.83rem; font-weight: 700; }
.score-bar-track { height: 7px; background: rgba(255,255,255,0.05); border-radius: 100px; overflow: hidden; }
.score-bar-fill  { height: 100%; border-radius: 100px; }

.flag-item {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 9px 14px;
    background: rgba(255,69,96,0.06); border-left: 2px solid var(--red);
    border-radius: 0 7px 7px 0; margin-bottom: 7px;
    font-size: 0.86rem; color: var(--tx-m); line-height: 1.5;
}
.finding-item {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 9px 14px;
    background: rgba(255,184,0,0.06); border-left: 2px solid var(--yellow);
    border-radius: 0 7px 7px 0; margin-bottom: 7px;
    font-size: 0.86rem; color: var(--tx-m); line-height: 1.5;
}
.meta-item {
    padding: 8px 14px;
    background: rgba(124,77,255,0.06); border-left: 2px solid var(--p);
    border-radius: 0 7px 7px 0; margin-bottom: 7px;
    font-size: 0.86rem; color: var(--tx-m);
}
.ai-box {
    background: rgba(124,77,255,0.06);
    border: 1px solid rgba(124,77,255,0.18); border-radius: var(--r);
    padding: 18px 22px; font-size: 0.9rem; line-height: 1.72; color: var(--tx-m);
}
.ai-box-lbl {
    font-size: 0.69rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--p-light); margin-bottom: 9px;
}
.section-hdr {
    font-family: var(--font-d); font-size: 1.05rem; font-weight: 700;
    color: var(--tx); margin: 18px 0 12px; display: flex; align-items: center; gap: 8px;
}

/* ══════════════════════════════════════════
   DASHBOARD
══════════════════════════════════════════ */
.dash-kpi {
    background: var(--card); border: 1px solid var(--border-s);
    border-radius: var(--r); padding: 22px 18px; text-align: center; transition: all 0.3s;
}
.dash-kpi:hover { border-color: var(--border); transform: translateY(-3px); box-shadow: var(--shadow); }
.dash-kpi-val {
    font-family: var(--font-d); font-size: 2.2rem; font-weight: 800; line-height: 1; margin-bottom: 6px;
}
.dash-kpi-lbl { font-size: 0.76rem; color: var(--tx-m); text-transform: uppercase; letter-spacing: 0.07em; font-weight: 500; }

/* ══════════════════════════════════════════
   FOOTER — Seamless, no background bleed
══════════════════════════════════════════ */
.footer-wrap {
    border-top: 1px solid rgba(124,77,255,0.14);
    padding: 48px 0 0;
    margin: 64px -28px -80px;
    padding-left: 28px; padding-right: 28px;
    /* No background-color — inherits the app gradient, blends perfectly */
}
/* Kill any Streamlit wrapper backgrounds around the footer columns */
.footer-wrap ~ [data-testid="stVerticalBlock"],
.footer-wrap + * {
    background: transparent !important;
}
.footer-brand-name {
    font-family: var(--font-d); font-size: 1.1rem; font-weight: 800;
    background: linear-gradient(135deg, var(--p-light), var(--s));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    margin-bottom: 10px;
}
.footer-brand-desc {
    font-size: 0.84rem; color: rgba(255,255,255,0.65);
    line-height: 1.65; max-width: 230px; margin-bottom: 18px;
}
.footer-contact { font-size: 0.81rem; color: rgba(255,255,255,0.5); line-height: 2.1; }
.footer-heading {
    font-size: 0.74rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: rgba(255,255,255,0.85); margin-bottom: 18px;
}
.footer-link-item {
    font-size: 0.84rem; color: rgba(255,255,255,0.58);
    margin-bottom: 10px; cursor: pointer; transition: color 0.2s;
}
.footer-link-item:hover { color: rgba(255,255,255,0.9); }
.footer-bottom {
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 30px -28px 0;
    padding: 16px 28px;
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 8px;
    background: rgba(0,0,0,0.15);
}
.footer-copy  { font-size: 0.78rem; color: rgba(255,255,255,0.4); }
.footer-team  { font-size: 0.8rem; color: var(--p-light); font-weight: 600; }

/* ══════════════════════════════════════════
   ABOUT PAGE
══════════════════════════════════════════ */
.about-hero {
    background: rgba(124,77,255,0.07);
    border: 1px solid rgba(124,77,255,0.18); border-radius: var(--r-lg);
    padding: 32px 30px; margin-bottom: 24px;
}
.roadmap-item {
    background: var(--card); border: 1px solid var(--border-s); border-radius: var(--r);
    padding: 18px 22px; margin-bottom: 8px;
    display: flex; align-items: flex-start; gap: 14px; transition: all 0.2s;
}
.roadmap-item:hover { border-color: var(--border); box-shadow: var(--shadow); }
.roadmap-dot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; margin-top: 5px; }
.roadmap-done    { background: var(--green); }
.roadmap-current { background: var(--p-light); }
.roadmap-future  { background: var(--tx-d); }
.roadmap-title   { font-weight: 700; font-size: 0.9rem; color: var(--tx); margin-bottom: 3px; }
.roadmap-desc    { font-size: 0.81rem; color: var(--tx-m); }
.tech-badge {
    display: inline-block;
    background: rgba(124,77,255,0.1); border: 1px solid rgba(124,77,255,0.22);
    color: var(--p-light); padding: 4px 10px; border-radius: 4px;
    font-size: 0.76rem; font-weight: 600; margin: 3px;
}
.info-card {
    background: var(--card); border: 1px solid var(--border-s); border-radius: var(--r);
    padding: 20px 22px; transition: all 0.3s;
}
.info-card:hover { border-color: var(--border); transform: translateY(-3px); box-shadow: var(--shadow); }
.info-card-title { font-weight: 700; font-size: 0.93rem; color: var(--tx); margin-bottom: 6px; }
.info-card-desc  { font-size: 0.82rem; color: var(--tx-m); line-height: 1.55; }

/* ══════════════════════════════════════════
   ANIMATIONS
══════════════════════════════════════════ */
@keyframes fadeInUp {
    from { opacity:0; transform:translateY(18px); }
    to   { opacity:1; transform:translateY(0); }
}
.fade-in   { animation: fadeInUp 0.48s ease both; }
.fade-in-2 { animation: fadeInUp 0.48s 0.1s ease both; }

@media (max-width: 768px) {
    .hero-stats { grid-template-columns: repeat(2, 1fr); }
    .hero-title { font-size: 6rem; }
    .footer-bottom { flex-direction: column; text-align: center; }
}

/* ══════════════════════════════════════════
   V2 — AGENT PIPELINE TRACE
══════════════════════════════════════════ */
.agent-pipeline {
    display: flex; gap: 0; align-items: stretch;
    background: var(--card); border: 1px solid var(--border-s);
    border-radius: var(--r); overflow: hidden; margin: 16px 0;
}
.agent-step {
    flex: 1; padding: 14px 10px; text-align: center;
    border-right: 1px solid var(--border-s); position: relative;
    transition: background 0.2s;
}
.agent-step:last-child { border-right: none; }
.agent-step.active { background: rgba(124,77,255,0.12); }
.agent-step-num {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--p-light); margin-bottom: 5px;
}
.agent-step-name {
    font-size: 0.76rem; font-weight: 600; color: var(--tx);
    line-height: 1.3;
}
.agent-step-status {
    font-size: 0.68rem; color: var(--green); margin-top: 4px;
}

/* ══════════════════════════════════════════
   V2 — CLAIM VERIFICATION CARDS
══════════════════════════════════════════ */
.claim-card {
    background: var(--card); border: 1px solid var(--border-s);
    border-radius: var(--r); padding: 16px 18px; margin-bottom: 10px;
    transition: all 0.2s;
}
.claim-card:hover { border-color: var(--border); }
.claim-verdict-badge {
    display: inline-block; font-size: 0.67rem; font-weight: 700;
    letter-spacing: 0.09em; text-transform: uppercase;
    padding: 3px 10px; border-radius: 4px; margin-bottom: 10px;
}
.claim-supported    { color: var(--green);    background: rgba(0,229,160,0.12);  border: 1px solid rgba(0,229,160,0.25);  }
.claim-contradicted { color: var(--red);      background: rgba(255,69,96,0.12);  border: 1px solid rgba(255,69,96,0.25);  }
.claim-unverified   { color: var(--yellow);   background: rgba(255,184,0,0.12);  border: 1px solid rgba(255,184,0,0.25);  }
.claim-partial      { color: var(--s);        background: rgba(0,207,255,0.10);  border: 1px solid rgba(0,207,255,0.20);  }
.claim-text { font-size: 0.88rem; color: var(--tx); margin-bottom: 8px; font-weight: 500; line-height: 1.5; }
.claim-reasoning { font-size: 0.81rem; color: var(--tx-m); line-height: 1.55; }
.claim-conf { font-size: 0.76rem; color: var(--tx-d); margin-top: 6px; }

/* ══════════════════════════════════════════
   V2 — REASONING CHAIN
══════════════════════════════════════════ */
.reasoning-chain {
    background: rgba(0,207,255,0.04); border: 1px solid rgba(0,207,255,0.12);
    border-radius: var(--r); padding: 18px 20px;
}
.reasoning-step {
    display: flex; gap: 14px; align-items: flex-start;
    padding: 9px 0; border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.85rem; color: var(--tx-m); line-height: 1.55;
}
.reasoning-step:last-child { border-bottom: none; }
.reasoning-num {
    width: 22px; height: 22px; border-radius: 50%;
    background: rgba(124,77,255,0.18); border: 1px solid rgba(124,77,255,0.3);
    font-size: 0.7rem; font-weight: 700; color: var(--p-light);
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}

/* ══════════════════════════════════════════
   V2 — LINGUISTIC SCORES GRID
══════════════════════════════════════════ */
.ling-grid {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 14px 0;
}
.ling-cell {
    background: var(--card); border: 1px solid var(--border-s);
    border-radius: var(--r-sm); padding: 14px 12px; text-align: center;
    transition: all 0.2s;
}
.ling-cell:hover { border-color: var(--border); }
.ling-val {
    font-family: var(--font-d); font-size: 1.5rem; font-weight: 800; line-height: 1;
    margin-bottom: 4px;
}
.ling-label { font-size: 0.72rem; color: var(--tx-d); text-transform: uppercase; letter-spacing: 0.07em; }

/* ══════════════════════════════════════════
   V2 — DOCUMENT VERIFICATION
══════════════════════════════════════════ */
.doc-type-badge {
    display: inline-block; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    padding: 4px 12px; border-radius: 4px; margin-bottom: 14px;
    background: rgba(0,207,255,0.1); border: 1px solid rgba(0,207,255,0.25);
    color: var(--s);
}
.template-field-row {
    display: flex; align-items: center; gap: 10px;
    padding: 7px 0; border-bottom: 1px solid var(--border-s);
    font-size: 0.84rem;
}
.template-field-row:last-child { border-bottom: none; }
.field-found   { color: var(--green);  }
.field-missing { color: var(--red);    }
.field-name    { color: var(--tx-m);   flex: 1; }

/* ══════════════════════════════════════════
   V2 — FEEDBACK / CONTINUOUS LEARNING
══════════════════════════════════════════ */
.feedback-panel {
    background: rgba(0,229,160,0.04); border: 1px solid rgba(0,229,160,0.15);
    border-radius: var(--r); padding: 18px 22px; margin-top: 18px;
}
.feedback-title {
    font-size: 0.85rem; font-weight: 700; color: var(--tx);
    margin-bottom: 12px; display: flex; align-items: center; gap: 8px;
}
.learning-bar {
    height: 4px; background: rgba(255,255,255,0.05);
    border-radius: 100px; overflow: hidden; margin-top: 6px;
}
.learning-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--green), var(--s));
    border-radius: 100px;
}

/* ══════════════════════════════════════════
   V2 — EVIDENCE PANEL
══════════════════════════════════════════ */
.evidence-panel {
    background: rgba(0,207,255,0.04); border: 1px solid rgba(0,207,255,0.12);
    border-radius: var(--r); padding: 16px 18px; margin-top: 10px;
}
.evidence-item {
    padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.83rem; color: var(--tx-m); line-height: 1.55;
}
.evidence-item:last-child { border-bottom: none; }
.evidence-source {
    display: inline-block; font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.07em; text-transform: uppercase;
    color: var(--s); margin-right: 8px;
}
.evidence-title { font-weight: 600; color: var(--tx); font-size: 0.85rem; }

/* ══════════════════════════════════════════
   V2 — FORENSIC DETAIL PANEL
══════════════════════════════════════════ */
.forensic-panel {
    background: var(--card); border: 1px solid var(--border-s);
    border-radius: var(--r); padding: 0; overflow: hidden;
}
.forensic-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 16px; border-bottom: 1px solid var(--border-s);
}
.forensic-row:last-child { border-bottom: none; }
.forensic-label { font-size: 0.83rem; color: var(--tx-m); font-weight: 500; }
.forensic-val   { font-size: 0.83rem; font-weight: 700; }
.forensic-score-chip {
    font-size: 0.72rem; font-weight: 700; padding: 3px 10px;
    border-radius: 100px; letter-spacing: 0.04em;
}
.chip-low    { background: rgba(0,229,160,0.12); color: var(--green); }
.chip-medium { background: rgba(255,184,0,0.12); color: var(--yellow); }
.chip-high   { background: rgba(255,69,96,0.12); color: var(--red); }

/* ══════════════════════════════════════════
   V2 — DASHBOARD ANALYTICS
══════════════════════════════════════════ */
.stat-trend {
    font-size: 0.72rem; font-weight: 600; margin-top: 4px;
}
.trend-up   { color: var(--green); }
.trend-down { color: var(--red); }
.trend-flat { color: var(--tx-d); }

</style>
"""