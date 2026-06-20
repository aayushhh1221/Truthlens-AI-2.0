"""TruthLens AI 2.0 — About Page."""
import streamlit as st
from components.footer import render_footer


def render_about():
    st.markdown(
        """
        <div style="padding:36px 0 24px;text-align:center">
          <div class="section-label">Our Story</div>
          <div class="section-title">About <span class="grad-text">TruthLens AI 2.0</span></div>
          <div class="section-subtitle" style="margin-bottom:0">
            From a single-prompt Gemini wrapper to a full multi-agent verification
            platform — built to combat misinformation, deepfakes, and credential fraud.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Mission + Vision
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(
            """
            <div class="about-hero" style="height:100%">
              <div style="width:40px;height:40px;margin-bottom:12px;display:flex;align-items:center;justify-content:center;background:rgba(124,77,255,0.12);border-radius:10px">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--p-light)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>
                </svg>
              </div>
              <div style="font-family:var(--font-d);font-size:1.15rem;font-weight:700;
                          color:var(--tx);margin-bottom:10px">Our Mission</div>
              <div style="font-size:0.9rem;color:var(--tx-m);line-height:1.7">
                To democratize fact-checking and media verification by making advanced,
                evidence-grounded AI detection tools accessible to everyone — journalists,
                researchers, educators, hiring teams, and the general public. We believe
                informed citizens — armed with explainable AI — are the best defense
                against misinformation.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            """
            <div class="about-hero" style="height:100%">
              <div style="width:40px;height:40px;margin-bottom:12px;display:flex;align-items:center;justify-content:center;background:rgba(124,77,255,0.12);border-radius:10px">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--p-light)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
                </svg>
              </div>
              <div style="font-family:var(--font-d);font-size:1.15rem;font-weight:700;
                          color:var(--tx);margin-bottom:10px">Our Vision</div>
              <div style="font-size:0.9rem;color:var(--tx-m);line-height:1.7">
                A world where synthetic media, fabricated claims, and forged credentials
                can be instantly identified — with full transparency into why. We envision
                TruthLens as a foundational layer of digital trust infrastructure, embedded
                in newsrooms, hiring pipelines, admissions offices, and public institutions.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr class='section-divider' style='margin:36px 0'>", unsafe_allow_html=True)

    # What changed in v2.0
    st.markdown(
        '<div style="font-family:var(--font-d);font-size:1.2rem;font-weight:700;'
        'color:var(--tx);margin-bottom:20px">What Changed in v2.0</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="info-card" style="height:100%">
              <div class="info-card-title">Before — v1.0</div>
              <div class="info-card-desc">
                User Input &rarr; Gemini Prompt &rarr; Result.<br><br>
                A single LLM call produced the entire verdict. No evidence retrieval,
                no independent forensic signals, no claim-level breakdown, and no
                persistent learning loop.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="info-card" style="height:100%;border-color:rgba(0,229,160,0.25)">
              <div class="info-card-title" style="color:var(--green)">Now — v2.0</div>
              <div class="info-card-desc">
                Input &rarr; Feature Extraction &rarr; Evidence Collection &rarr; Claim
                Verification &rarr; Multi-Agent Reasoning &rarr; Risk Scoring &rarr;
                Explainable Output &rarr; Continuous Learning.<br><br>
                Twelve local forensic signals, RAG-grounded evidence, six specialized
                agents, a structured explainability report, and a SQLite-backed
                feedback loop.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr class='section-divider' style='margin:36px 0'>", unsafe_allow_html=True)

    # Module Architecture
    st.markdown(
        '<div style="font-family:var(--font-d);font-size:1.2rem;font-weight:700;'
        'color:var(--tx);margin-bottom:20px">Module Architecture</div>',
        unsafe_allow_html=True,
    )

    modules = [
        ("frontend / pages",    "Streamlit pages and components — navbar, score bars, claim cards, dashboards."),
        ("agents",              "Six-agent orchestration: extractor, evidence finder, fact checker, risk assessor, explainer, judge."),
        ("rag",                 "Evidence retrieval pipeline — Wikipedia + Google Custom Search, semantic re-ranking."),
        ("forensics",           "Text linguistics, embedding similarity, image ELA/EXIF/noise/edge, and document forensics."),
        ("models",              "Top-level analyzers that orchestrate forensics + agents + persistence for each content type."),
        ("explainability",      "Builds the structured explainability report — evidence, confidence, reasoning chain, sources."),
        ("database",            "SQLite schema and ORM-style helpers for users, analyses, claims, evidence, feedback, documents."),
        ("analytics",           "Continuous-learning helpers — dataset export, retraining readiness, model versioning."),
        ("verification",        "Claim verification pipeline (Agent 3) — evidence-grounded SUPPORTED/CONTRADICTED/UNVERIFIED labels."),
        ("backend (app.py)",    "Routing, session state, and database initialization for the whole platform."),
    ]
    mc1, mc2 = st.columns(2)
    for i, (name, desc) in enumerate(modules):
        col = mc1 if i % 2 == 0 else mc2
        with col:
            st.markdown(
                f"""
                <div style="display:flex;align-items:flex-start;gap:14px;padding:12px 0;
                             border-bottom:1px solid var(--border-s)">
                  <div style="font-family:var(--font-d);font-weight:800;font-size:0.78rem;
                              color:var(--p-light);min-width:118px;padding-top:2px;
                              text-transform:lowercase">/{name}</div>
                  <div style="font-size:0.83rem;color:var(--tx-m);line-height:1.6">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<hr class='section-divider' style='margin:36px 0'>", unsafe_allow_html=True)

    # Tech stack + Impact
    col_tech, col_impact = st.columns([1, 1])

    with col_tech:
        st.markdown(
            '<div style="font-family:var(--font-d);font-size:1.1rem;font-weight:700;'
            'color:var(--tx);margin-bottom:18px">Technology Stack</div>',
            unsafe_allow_html=True,
        )
        tech_items = [
            ("""<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--p-light)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>""", "Google Gemini 2.0", "Multimodal reasoning, vision analysis, and JSON-structured agent calls"),
            ("""<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--p-light)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>""", "Python 3.10+", "Core backend, agents, and forensics pipelines"),
            ("""<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--p-light)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>""", "Streamlit", "Full-stack web framework and UI runtime"),
            ("""<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--p-light)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>""", "Sentence Transformers", "all-MiniLM-L6-v2 for semantic similarity &amp; claim clustering"),
            ("""<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--p-light)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>""", "Wikipedia + Google CSE", "RAG evidence retrieval for claim verification"),
            ("""<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--p-light)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>""", "Pillow + NumPy/SciPy", "ELA, noise, compression, and edge forensic analysis"),
            ("""<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--p-light)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>""", "Pytesseract + pypdf", "OCR and PDF text extraction for document verification"),
            ("""<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--p-light)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>""", "SQLite", "Users, analyses, claims, evidence, feedback, documents, model versions"),
            ("""<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--p-light)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>""", "Plotly", "Interactive gauges, radar charts, donuts, and trend lines"),
        ]
        for icon, tech, desc in tech_items:
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:14px;padding:12px 0;
                             border-bottom:1px solid var(--border-s)">
                  <div style="width:32px;height:32px;min-width:32px;display:flex;align-items:center;
                              justify-content:center;background:rgba(124,77,255,0.10);border-radius:8px">{icon}</div>
                  <div>
                    <div style="font-weight:700;font-size:0.9rem;color:var(--tx)">{tech}</div>
                    <div style="font-size:0.78rem;color:var(--tx-d)">{desc}</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_impact:
        st.markdown(
            '<div style="font-family:var(--font-d);font-size:1.1rem;font-weight:700;'
            'color:var(--tx);margin-bottom:18px">Platform Capabilities</div>',
            unsafe_allow_html=True,
        )
        impact_items = [
            ("6",   "specialized AI agents in the reasoning pipeline"),
            ("12",  "independent forensic signals (linguistic + image)"),
            ("3",   "detection modes — text, image, document"),
            ("8",   "database tables tracking the full feedback loop"),
            ("100", "feedback samples targeted before recalibration"),
        ]
        for val, lbl in impact_items:
            st.markdown(
                f"""
                <div style="display:flex;align-items:baseline;gap:10px;padding:12px 0;
                             border-bottom:1px solid var(--border-s)">
                  <div style="font-family:var(--font-d);font-size:1.35rem;font-weight:800;
                               background:linear-gradient(135deg,var(--p-light),var(--s));
                               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                               background-clip:text;min-width:56px">{val}</div>
                  <div style="font-size:0.84rem;color:var(--tx-m)">{lbl}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        st.markdown(
            '<div style="font-family:var(--font-d);font-size:1.1rem;font-weight:700;'
            'color:var(--tx);margin-bottom:18px">Judge Feedback &rarr; v2.0 Response</div>',
            unsafe_allow_html=True,
        )
        feedback_map = [
            ("AI reasoning needs to go deeper",            "6-agent pipeline with claim-level reasoning chains"),
            ("AI should learn from verification data",     "SQLite feedback loop + retraining-readiness tracker"),
            ("Need learned pattern recognition",            "Sentence-embedding claim clustering &amp; similarity"),
            ("Need specific forgery-detection signals",     "ELA, EXIF, noise, compression, edge analysis"),
            ("Too dependent on LLM reasoning",              "12 local signals computed with zero LLM calls"),
        ]
        for issue, resp in feedback_map:
            st.markdown(
                f"""
                <div style="padding:8px 0;border-bottom:1px solid var(--border-s);font-size:0.8rem">
                  <div style="color:var(--tx-d)">{issue}</div>
                  <div style="color:var(--green);margin-top:2px">&rarr; {resp}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<hr class='section-divider' style='margin:36px 0'>", unsafe_allow_html=True)

    # Roadmap
    st.markdown(
        '<div style="font-family:var(--font-d);font-size:1.2rem;font-weight:700;'
        'color:var(--tx);margin-bottom:20px">Product Roadmap</div>',
        unsafe_allow_html=True,
    )

    roadmap = [
        ("done",    "v1.0 — Core Platform",
         "Fake news text detection, deepfake image analysis, analytics dashboard, team page."),
        ("done",    "v1.1 — UI Redesign",
         "Premium SaaS-grade UI redesign with SatyaSetu-inspired design language."),
        ("done",    "v2.0 — Multi-Agent Architecture",
         "6-agent pipeline, RAG evidence retrieval, 12 forensic signals, document verification, "
         "explainability reports, and SQLite-backed continuous learning."),
        ("current", "v2.1 — Video Deepfake Detection (In Progress)",
         "Extend deepfake detection to video files using frame-level ELA and Gemini Vision."),
        ("current", "v2.2 — URL / Article Scanner (In Progress)",
         "Scan any URL or web article end-to-end without manual copy-pasting."),
        ("future",  "v2.3 — Audio Deepfake Detection",
         "Detect AI-cloned voices and synthetic audio in podcasts and news clips."),
        ("future",  "v2.4 — Browser Extension",
         "One-click fact-checking directly in the browser while reading news."),
        ("future",  "v3.0 — Real-time Monitoring API",
         "REST API for organisations and newsrooms to integrate TruthLens into existing workflows."),
    ]
    for status, title, desc in roadmap:
        dot_cls = f"roadmap-{status}"
        st.markdown(
            f"""
            <div class="roadmap-item">
              <div class="roadmap-dot {dot_cls}"></div>
              <div>
                <div class="roadmap-title">{title}</div>
                <div class="roadmap-desc">{desc}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr class='section-divider' style='margin:36px 0'>", unsafe_allow_html=True)

    # Open source + Acknowledgements
    st.markdown(
        """
        <div style="text-align:center;padding:28px;background:var(--card);
                    border:1px solid var(--border-s);border-radius:var(--r-lg)">
          <div style="display:flex;justify-content:center;margin-bottom:12px">
            <div style="width:44px;height:44px;display:flex;align-items:center;justify-content:center;
                        background:rgba(124,77,255,0.12);border-radius:12px">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--p-light)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
            </div>
          </div>
          <div style="font-family:var(--font-d);font-size:1.1rem;font-weight:700;color:var(--tx);margin-bottom:8px">
            Open Source &amp; Community-Driven
          </div>
          <div style="font-size:0.88rem;color:var(--tx-m);max-width:560px;margin:0 auto;line-height:1.7">
            TruthLens AI is built with open-source tools and is committed to transparent,
            explainable AI. We believe the fight against misinformation must itself be open and
            accountable. Contributions are welcome.
          </div>
          <div style="margin-top:16px">
            <span class="tech-badge">Python</span>
            <span class="tech-badge">Streamlit</span>
            <span class="tech-badge">Gemini 2.0</span>
            <span class="tech-badge">Sentence Transformers</span>
            <span class="tech-badge">SQLite</span>
            <span class="tech-badge">Plotly</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_footer()
