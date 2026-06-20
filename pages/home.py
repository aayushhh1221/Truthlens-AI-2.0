"""TruthLens AI 2.0 — Home / Landing Page. Emoji-free, enterprise design."""
import streamlit as st
from components.footer import render_footer


def _nav(page: str):
    st.session_state.page = page
    st.rerun()


def render_home():
    # ── SECTION 1: HERO ──────────────────────────────────────
    st.markdown(
        """
        <div class="hero-wrap fade-in">
          <div class="hero-eyebrow">Multi-Agent AI &middot; Powered by Google Gemini 2.0</div>
          <h1 class="hero-title">TruthLens AI 2.0</h1>
          <p class="hero-desc" style="text-align:center;margin-left:auto;margin-right:auto;">
            A complete misinformation, deepfake, and document-forgery verification platform.
            Six specialized AI agents extract claims, retrieve evidence, fact-check,
            assess risk, and explain every verdict — grounded in real forensic signals,
            not just LLM guesses.
          </p>
          <div class="hero-cta">
            <span class="btn-hero-primary">Analyze Text</span>
            <span class="btn-hero-outline">Detect Deepfake</span>
            <span class="btn-hero-outline">Verify Document</span>
          </div>
          <div class="hero-stats">
            <div class="hero-stat">
              <div class="hero-stat-val">6</div>
              <div class="hero-stat-lbl">AI Agents</div>
            </div>
            <div class="hero-stat">
              <div class="hero-stat-val">12</div>
              <div class="hero-stat-lbl">Forensic Signals</div>
            </div>
            <div class="hero-stat">
              <div class="hero-stat-val">3</div>
              <div class="hero-stat-lbl">Detection Modes</div>
            </div>
            <div class="hero-stat">
              <div class="hero-stat-val">RAG</div>
              <div class="hero-stat-lbl">Evidence Retrieval</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b, col_c, col_d, col_e = st.columns([1.5, 1, 1, 1, 1.5])
    with col_b:
        if st.button("Analyze Text", key="hero_fn", use_container_width=True):
            _nav("Detection")
    with col_c:
        if st.button("Detect Deepfake", key="hero_df", use_container_width=True):
            _nav("Detection")
    with col_d:
        if st.button("Verify Document", key="hero_doc", use_container_width=True):
            _nav("Documents")

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── SECTION 2: THE PROBLEM ───────────────────────────────
    st.markdown(
        """
        <div style="text-align:center;margin-bottom:40px">
          <div class="section-label">The Challenge We Solve</div>
          <div class="section-title">Misinformation Is a <span class="grad-text">Global Crisis</span></div>
          <div class="section-subtitle">
            The spread of fake news, deepfakes, and forged credentials is eroding public
            trust and distorting reality at an unprecedented scale.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pc1, pc2, pc3, pc4 = st.columns(4)
    problems = [
        ("red",    "SPREAD RATE",    "6x",   "Misinformation Spread",
         "False content spreads roughly six times faster than factual content on social platforms."),
        ("yellow", "SCALE",          "3.2B", "Deepfake Threats",
         "Billions of synthetic media files are now in circulation — manipulation is no longer rare."),
        ("purple", "PUBLIC CONCERN", "85%",  "Trust Deficit",
         "Most people report difficulty distinguishing real content from AI-generated or doctored media."),
        ("cyan",   "CREDENTIAL FRAUD","1in5","Forged Documents",
         "Forged certificates and IDs remain a persistent vector for fraud across hiring and admissions."),
    ]
    for col, (stat_cls, tag_lbl, stat, title, desc) in zip([pc1, pc2, pc3, pc4], problems):
        with col:
            st.markdown(
                f"""
                <div class="problem-card">
                  <div class="prob-tag prob-tag-{stat_cls}">{tag_lbl}</div>
                  <div class="prob-title">{title}</div>
                  <div class="prob-desc">{desc}</div>
                  <div class="prob-stat prob-stat-{stat_cls}">{stat}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="why-matters">
          <div>
            <div class="why-matters-title">Why TruthLens 2.0 is different</div>
            <div class="why-matters-desc">
              Most "AI fact-checkers" are a single LLM prompt. TruthLens 2.0 is a pipeline:
              independent linguistic forensics, RAG-grounded evidence retrieval, multi-agent
              fact-checking, and a transparent reasoning chain for every verdict.
            </div>
          </div>
          <div class="why-matters-tags">
            <span class="wm-tag wm-tag-cyan">Evidence-Grounded</span>
            <span class="wm-tag wm-tag-purple">Multi-Agent</span>
            <span class="wm-tag wm-tag-green">Explainable</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── SECTION 3: PIPELINE ARCHITECTURE ─────────────────────
    st.markdown(
        """
        <div style="text-align:center;margin-bottom:40px">
          <div class="section-label">System Architecture</div>
          <div class="section-title">From <span class="grad-text">Input</span> to <span class="grad-text">Verdict</span></div>
          <div class="section-subtitle">
            Every piece of content flows through the same eight-stage pipeline —
            no shortcuts, no single-prompt black boxes.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    s1, s2, s3, s4 = st.columns(4)
    s5, s6, s7, s8 = st.columns(4)
    steps = [
        ("01", "Feature Extraction",
         "Linguistic signals — clickbait, emotional tone, urgency, certainty, propaganda — computed locally, no LLM required."),
        ("02", "Evidence Collection",
         "RAG pipeline queries Wikipedia and web search for evidence relevant to each extracted claim."),
        ("03", "Claim Verification",
         "Each claim is checked against retrieved evidence and classified as supported, contradicted, or unverified."),
        ("04", "Multi-Agent Reasoning",
         "Six agents — extractor, evidence finder, fact-checker, risk assessor, explainer, and judge — collaborate on the verdict."),
        ("05", "Risk Scoring",
         "Linguistic risk and claim-verification risk are combined into a single, calibrated fake score."),
        ("06", "Explainable Reasoning",
         "A step-by-step reasoning chain shows exactly how the verdict was reached — no black box."),
        ("07", "Continuous Learning",
         "User feedback (Correct / Incorrect) is logged and tracked toward future model retraining."),
        ("08", "Forensics & Documents",
         "Images get ELA, EXIF, noise, and edge analysis; documents get OCR, template matching, and forgery scoring."),
    ]
    for col, (num, title, desc) in zip([s1, s2, s3, s4, s5, s6, s7, s8], steps):
        with col:
            st.markdown(
                f"""
                <div class="step-card">
                  <div class="step-num-badge">STAGE {num}</div>
                  <div class="step-title">{title}</div>
                  <div class="step-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── SECTION 4: CORE TECHNOLOGIES ────────────────────────
    st.markdown(
        """
        <div style="text-align:center;margin-bottom:40px">
          <div class="section-label">Core Capabilities</div>
          <div class="section-title">Three Detection <span class="grad-text">Engines</span></div>
          <div class="section-subtitle">
            Working together to tackle misinformation at every layer — text, visual media,
            and official documents.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        st.markdown(
            """
            <div class="feature-card">
              <div class="fc-label">Text Intelligence</div>
              <div class="fc-title">Misinformation Detection</div>
              <div class="fc-sub">
                Linguistic forensics combined with RAG-grounded multi-agent fact-checking
                for deep, evidence-based verdicts.
              </div>
              <ul class="fc-list">
                <li class="fc-item"><span class="fc-check">&#10003;</span> Clickbait / Propaganda Scoring</li>
                <li class="fc-item"><span class="fc-check">&#10003;</span> Claim Extraction &amp; Verification</li>
                <li class="fc-item"><span class="fc-check">&#10003;</span> Wikipedia + Web Evidence Retrieval</li>
                <li class="fc-item"><span class="fc-check">&#10003;</span> 6-Agent Reasoning Pipeline</li>
                <li class="fc-item"><span class="fc-check">&#10003;</span> Explainable Reasoning Chains</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Try Text Detection", key="cta_fn", use_container_width=True):
            _nav("Detection")

    with fc2:
        st.markdown(
            """
            <div class="feature-card">
              <div class="fc-label">Vision Intelligence</div>
              <div class="fc-title">Deepfake &amp; Image Forensics</div>
              <div class="fc-sub">
                Real pixel-level forensic signals combined with Gemini Vision AI —
                not Gemini-only analysis.
              </div>
              <ul class="fc-list">
                <li class="fc-item"><span class="fc-check">&#10003;</span> Error Level Analysis (ELA)</li>
                <li class="fc-item"><span class="fc-check">&#10003;</span> EXIF &amp; Metadata Forensics</li>
                <li class="fc-item"><span class="fc-check">&#10003;</span> Noise &amp; Compression Analysis</li>
                <li class="fc-item"><span class="fc-check">&#10003;</span> Edge Consistency Detection</li>
                <li class="fc-item"><span class="fc-check">&#10003;</span> Gemini Vision AI Cross-Check</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Try Image Detection", key="cta_df", use_container_width=True):
            _nav("Detection")

    with fc3:
        st.markdown(
            """
            <div class="feature-card">
              <div class="fc-label">Document Intelligence</div>
              <div class="fc-title">Credential Verification</div>
              <div class="fc-sub">
                OCR-driven template matching and AI forgery detection for certificates,
                IDs, and academic documents.
              </div>
              <ul class="fc-list">
                <li class="fc-item"><span class="fc-check">&#10003;</span> OCR Text Extraction</li>
                <li class="fc-item"><span class="fc-check">&#10003;</span> Template Field Matching</li>
                <li class="fc-item"><span class="fc-check">&#10003;</span> Date &amp; Font Consistency Checks</li>
                <li class="fc-item"><span class="fc-check">&#10003;</span> AI-Powered Forgery Detection</li>
                <li class="fc-item"><span class="fc-check">&#10003;</span> Authenticity Scoring</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Try Document Verification", key="cta_doc", use_container_width=True):
            _nav("Documents")

    st.markdown(
        """
        <div class="integration-bar" style="margin-top:14px">
          <div class="ib-left">
            <div>
              <div class="ib-title">Unified Platform</div>
              <div class="ib-desc">Text, image, and document engines share one database, one analytics dashboard, and one feedback loop.</div>
            </div>
          </div>
          <span class="ib-link">View Architecture &rarr;</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── SECTION 5: MULTI-AGENT SYSTEM ───────────────────────
    st.markdown(
        """
        <div style="text-align:center;margin-bottom:40px">
          <div class="section-label">Multi-Agent System</div>
          <div class="section-title">Six Agents, <span class="grad-text">One Verdict</span></div>
          <div class="section-subtitle">
            Each agent has a single responsibility — together they produce a verdict
            that's grounded, explainable, and reproducible.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    a1, a2, a3 = st.columns(3)
    a4, a5, a6 = st.columns(3)
    agents = [
        ("01", "Claim Extractor",      "Identifies verifiable factual claims — statistics, named entities, events — from raw text."),
        ("02", "Evidence Finder",      "Runs the RAG pipeline against Wikipedia and web search to retrieve supporting or contradicting evidence."),
        ("03", "Fact Checker",         "Compares each claim against retrieved evidence and classifies it as supported, contradicted, or unverified."),
        ("04", "Risk Assessor",        "Combines linguistic risk and claim-verification outcomes into a calibrated fake score and risk level."),
        ("05", "Explainability Agent", "Builds a human-readable, step-by-step reasoning chain explaining exactly why the verdict was reached."),
        ("06", "Final Judge",          "Synthesizes all agent outputs into the final verdict, trust score, and confidence rating."),
    ]
    for col, (num, title, desc) in zip([a1, a2, a3, a4, a5, a6], agents):
        with col:
            st.markdown(
                f"""
                <div class="why-card">
                  <div class="wc-index">Agent {num}</div>
                  <div class="wc-title">{title}</div>
                  <div class="wc-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── SECTION 6: WHY TRUTHLENS ─────────────────────────────
    st.markdown(
        """
        <div style="text-align:center;margin-bottom:40px">
          <div class="section-label">Advantages</div>
          <div class="section-title">Why <span class="grad-text">TruthLens 2.0</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    w1, w2, w3 = st.columns(3)
    w4, w5, w6 = st.columns(3)
    why_items = [
        ("01", "Evidence-Grounded",     "Every verdict is checked against real evidence via RAG — not just LLM intuition."),
        ("02", "Real Forensic Signals", "Image analysis includes ELA, noise, EXIF, and edge detection — independent of Gemini."),
        ("03", "Explainable AI",        "A transparent reasoning chain accompanies every verdict — no black-box outputs."),
        ("04", "Continuous Learning",   "User feedback is logged and tracked toward model improvement over time."),
        ("05", "Credential Verification","Beyond text and images — TruthLens also verifies certificates, IDs, and degrees."),
        ("06", "Local-First Database",  "SQLite-backed analytics track every analysis, claim, and feedback signal."),
    ]
    for col, (idx, title, desc) in zip([w1, w2, w3, w4, w5, w6], why_items):
        with col:
            st.markdown(
                f"""
                <div class="why-card">
                  <div class="wc-index">{idx}</div>
                  <div class="wc-title">{title}</div>
                  <div class="wc-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ── SECTION 7: TEAM ─────────────────────────────────────
    _render_team_cards()

    # ── SECTION 8: FOOTER ────────────────────────────────────
    render_footer()


def _render_team_cards():
    st.markdown(
        """
        <div class="team-section-title">Meet Our Team</div>
        <div class="team-section-sub">
            The people behind TruthLens AI &mdash; Team HackManthan, DDUGU Gorakhpur
        </div>
        """,
        unsafe_allow_html=True,
    )

    members = [
        {
            "initials": "SK",
            "name": "Sujal Kumar Patwa",
            "role": "Team Lead &amp; AI/ML Engineer",
            "responsibilities": [
                "Project architecture and technical direction",
                "Multi-agent pipeline and risk-scoring design",
                "Gemini API integration and prompt engineering",
                "Research methodology and model evaluation",
            ],
            "skills": ["Python", "Gemini AI", "Multi-Agent", "ML"],
            "lead": True,
            "github": "https://github.com/Sujal-CSE25",
            "linkedin": "https://www.linkedin.com/in/sujal-kumar-ddu/",
        },
        {
            "initials": "AM",
            "name": "Aayush Mani Tripathi",
            "role": "Backend &amp; AI/ML Developer",
            "responsibilities": [
                "Backend architecture, database, and API design",
                "RAG evidence-retrieval pipeline",
                "ML pipeline integration and optimization",
                "Server-side logic and data flow design",
            ],
            "skills": ["Python", "SQLite", "RAG", "APIs"],
            "lead": False,
            "github": "https://github.com/aayushhh1221",
            "linkedin": "https://www.linkedin.com/in/aayush-mani-tripathi-97a767382/",
        },
        {
            "initials": "ON",
            "name": "Om Narayan",
            "role": "Frontend &amp; UI Developer",
            "responsibilities": [
                "UI architecture and Streamlit frontend",
                "Component system and design implementation",
                "Dashboard and analytics visualizations",
                "CSS design language and visual polish",
            ],
            "skills": ["Streamlit", "CSS", "UX", "Plotly"],
            "lead": False,
            "github": "https://github.com/Om-CSE25",
            "linkedin": "https://www.linkedin.com/in/om-narayana-cse/",
        },
        {
            "initials": "RK",
            "name": "Ritesh Kumar Gautam",
            "role": "Image AI &amp; QA Engineer",
            "responsibilities": [
                "Image forensics engine (ELA, noise, edge)",
                "Gemini Vision AI integration",
                "End-to-end testing and validation",
                "QA workflows and bug triage",
            ],
            "skills": ["CV", "Gemini Vision", "PIL", "QA"],
            "lead": False,
            "github": "https://github.com/CodeWithRitesh-Collab",
            "linkedin": "https://in.linkedin.com/in/ritesh-gautam-er",
        },
    ]

    t1, t2, t3, t4 = st.columns(4)
    for col, m in zip([t1, t2, t3, t4], members):
        resp_items = "".join(
            f'<li class="tc-resp-item"><span class="tc-resp-dot"></span>{r}</li>'
            for r in m["responsibilities"]
        )
        skill_badges = "".join(
            f'<span class="tc-badge">{s}</span>' for s in m["skills"]
        )
        lead_badge = (
            '<span class="tc-badge tc-badge-lead">Team Lead</span>' if m["lead"] else ""
        )
        with col:
            st.markdown(
                f"""
                <div class="team-card">
                  <div class="tc-header">
                    <div class="tc-avatar">{m['initials']}</div>
                    <div class="tc-social">
                      <a class="tc-social-link" href="{m['github']}" target="_blank" rel="noopener noreferrer" title="GitHub">GH</a>
                      <a class="tc-social-link" href="{m['linkedin']}" target="_blank" rel="noopener noreferrer" title="LinkedIn">in</a>
                    </div>
                  </div>
                  <div class="tc-name">{m['name']}</div>
                  <div class="tc-role">{m['role']}</div>
                  <div class="tc-resp-title">Responsibilities</div>
                  <ul class="tc-resp-list">{resp_items}</ul>
                  <div class="tc-badge-row">{lead_badge}{skill_badges}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )