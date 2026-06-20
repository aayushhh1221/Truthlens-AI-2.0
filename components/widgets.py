"""
TruthLens AI 2.0 — Reusable UI Widgets
"""
import streamlit as st
from utils.helpers import clamp


# ─── Verdict Banner ──────────────────────────────────────────

def render_verdict(verdict: str):
    verdict_upper = (verdict or "UNCERTAIN").upper()
    fake_verdicts = {"LIKELY FAKE", "LIKELY AI-GENERATED", "DEEPFAKE SUSPECTED",
                     "LIKELY MANIPULATED", "LIKELY FORGED"}
    real_verdicts = {"LIKELY REAL", "LIKELY AUTHENTIC"}

    if any(v in verdict_upper for v in fake_verdicts):
        css_class = "verdict-fake"
        icon = "✕"
        sub  = "High Risk Detected"
    elif any(v in verdict_upper for v in real_verdicts):
        css_class = "verdict-real"
        icon = "✓"
        sub  = "Content Appears Authentic"
    else:
        css_class = "verdict-uncertain"
        icon = "?"
        sub  = "Further Verification Recommended"

    st.markdown(
        f"""
        <div class="{css_class}">
          <div style="width:42px;height:42px;border-radius:50%;display:flex;align-items:center;
                      justify-content:center;font-size:1.2rem;font-weight:900;flex-shrink:0;
                      background:rgba(255,255,255,0.08)">{icon}</div>
          <div>
            <div class="verdict-sub">{sub}</div>
            <div style="font-size:1.15rem;font-weight:800;">{verdict_upper}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─── Score Bar ───────────────────────────────────────────────

def score_bar(label: str, value: float, tooltip: str = "", invert: bool = False):
    """Render a labelled progress bar."""
    val = int(clamp(value))
    display_val = (100 - val) if invert else val

    if display_val >= 70:
        color = "#FF4560"
    elif display_val >= 40:
        color = "#FFB800"
    else:
        color = "#00E5A0"

    st.markdown(
        f"""
        <div class="score-bar-wrap" title="{tooltip}">
          <div class="score-bar-hdr">
            <span class="score-bar-lbl">{label}</span>
            <span class="score-bar-num" style="color:{color}">{display_val}</span>
          </div>
          <div class="score-bar-track">
            <div class="score-bar-fill" style="width:{display_val}%;background:{color}"></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─── Score Row (KPI strip) ───────────────────────────────────

def score_row(result: dict):
    fake  = int(clamp(result.get("fake_score", 0)))
    trust = int(clamp(result.get("trust_score", 0)))
    bias  = int(clamp(result.get("bias_score", 0)))
    manip = int(clamp(result.get("manipulation_score", 0)))

    def _color(v): return "#FF4560" if v >= 70 else ("#FFB800" if v >= 40 else "#00E5A0")

    cols = st.columns(4)
    for col, (lbl, val) in zip(cols, [("Fake Score", fake), ("Trust Score", trust),
                                        ("Bias Score", bias), ("Manipulation", manip)]):
        with col:
            st.markdown(
                f"""
                <div class="dash-kpi">
                  <div class="dash-kpi-val" style="color:{_color(val)}">{val}</div>
                  <div class="dash-kpi-lbl">{lbl}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ─── Linguistic Scores Grid ──────────────────────────────────

def render_linguistic_scores(ling: dict):
    """
    Render the 5 required linguistic signals (Phase 2A) plus credibility.

    NOTE: `ling` here is `result["linguistic_scores"]` as built by
    agents/multi_agent.py's FinalJudgeAgent, which uses NON-suffixed keys:
    clickbait, emotional, urgency, certainty, propaganda, credibility.
    """
    def _risk_color(v):
        # Higher = more risky
        return "#FF4560" if v >= 70 else ("#FFB800" if v >= 40 else "#00E5A0")

    def _good_color(v):
        # Higher = better (e.g. credibility)
        return "#00E5A0" if v >= 60 else ("#FFB800" if v >= 30 else "#FF4560")

    scores = [
        ("Clickbait",   ling.get("clickbait", 0),   _risk_color),
        ("Emotional",   ling.get("emotional", 0),   _risk_color),
        ("Urgency",     ling.get("urgency", 0),     _risk_color),
        ("Propaganda",  ling.get("propaganda", 0),  _risk_color),
        ("Certainty",   ling.get("certainty", 0),   _risk_color),
        ("Credibility", ling.get("credibility", 0), _good_color),
    ]

    cells = "".join([
        f"""<div class="ling-cell">
              <div class="ling-val" style="color:{color_fn(v)}">{int(v)}</div>
              <div class="ling-label">{lbl}</div>
            </div>"""
        for lbl, v, color_fn in scores
    ])
    st.markdown(f'<div class="ling-grid">{cells}</div>', unsafe_allow_html=True)


# ─── Agent Pipeline Trace ─────────────────────────────────────

def render_agent_trace(trace: list):
    if not trace:
        return
    steps_html = ""
    for i, step in enumerate(trace):
        agent = step.get("agent", f"Agent {i+1}")
        status = "Complete"
        extra  = ""
        if "claims_found" in step:
            extra = f"{step['claims_found']} claims"
        elif "sources_searched" in step:
            extra = f"{step['sources_searched']} sources"
        elif "claims_verified" in step:
            extra = f"{step['claims_verified']} verified"
        elif "verdict" in step:
            extra = step["verdict"]
        steps_html += f"""
        <div class="agent-step active">
          <div class="agent-step-num">Agent {i+1}</div>
          <div class="agent-step-name">{agent}</div>
          <div class="agent-step-status">{extra or status}</div>
        </div>"""

    st.markdown(
        f"""
        <div style="font-size:0.8rem;font-weight:700;color:var(--tx-d);
                    text-transform:uppercase;letter-spacing:0.09em;margin-bottom:8px">
          Multi-Agent Pipeline
        </div>
        <div class="agent-pipeline">{steps_html}</div>
        """,
        unsafe_allow_html=True,
    )


# ─── Claim Verification Cards ─────────────────────────────────

def render_claim_cards(verified_claims: list):
    if not verified_claims:
        return
    section_header("Claim Verification", "")

    verdict_map = {
        "SUPPORTED":     ("claim-supported",    "Supported"),
        "CONTRADICTED":  ("claim-contradicted",  "Contradicted"),
        "UNVERIFIED":    ("claim-unverified",    "Unverified"),
        "PARTIALLY_TRUE":("claim-partial",       "Partially True"),
    }

    for claim in verified_claims[:6]:
        v = (claim.get("verdict") or "UNVERIFIED").upper()
        css_cls, lbl = verdict_map.get(v, ("claim-unverified", v))
        conf = claim.get("confidence", 0)
        reasoning = claim.get("reasoning", "")
        claim_text = claim.get("claim", "")[:200]

        st.markdown(
            f"""
            <div class="claim-card">
              <div class="claim-verdict-badge {css_cls}">{lbl}</div>
              <div class="claim-text">{claim_text}</div>
              {f'<div class="claim-reasoning">{reasoning}</div>' if reasoning else ''}
              <div class="claim-conf">Confidence: {conf}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ─── Reasoning Chain ─────────────────────────────────────────

def render_reasoning_chain(chain: list):
    if not chain:
        return
    section_header("AI Reasoning Chain", "")
    steps = "".join([
        f'<div class="reasoning-step"><div class="reasoning-num">{i+1}</div><div>{step}</div></div>'
        for i, step in enumerate(chain)
    ])
    st.markdown(f'<div class="reasoning-chain">{steps}</div>', unsafe_allow_html=True)


# ─── Flags / Findings ────────────────────────────────────────

def render_flags(flags: list, title: str = "Risk Signals"):
    if not flags:
        return
    section_header(title, "")
    for f in flags[:8]:
        st.markdown(f'<div class="flag-item"><span style="color:var(--red);font-size:0.75rem">&#9679;</span>{f}</div>',
                    unsafe_allow_html=True)


def render_findings(findings: list, title: str = "Forensic Findings"):
    if not findings:
        return
    section_header(title, "")
    for f in findings[:8]:
        st.markdown(f'<div class="finding-item"><span style="color:var(--yellow);font-size:0.75rem">&#9679;</span>{f}</div>',
                    unsafe_allow_html=True)


def render_meta_flags(flags: list):
    if not flags:
        return
    section_header("Metadata Flags", "")
    for f in flags[:6]:
        st.markdown(f'<div class="meta-item">{f}</div>', unsafe_allow_html=True)


# ─── AI Explanation ──────────────────────────────────────────

def ai_explanation(text: str):
    if not text:
        return
    section_header("AI Analysis", "")
    st.markdown(
        f"""
        <div class="ai-box">
          <div class="ai-box-lbl">Reasoning</div>
          {text}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─── Forensic Detail Panel ───────────────────────────────────

def render_forensic_detail(forensics: dict):
    if not forensics:
        return
    section_header("Forensic Breakdown", "")

    def chip(score):
        if score >= 70:
            return f'<span class="forensic-score-chip chip-high">{score}/100 HIGH</span>'
        elif score >= 40:
            return f'<span class="forensic-score-chip chip-medium">{score}/100 MEDIUM</span>'
        return f'<span class="forensic-score-chip chip-low">{score}/100 LOW</span>'

    ela   = forensics.get("ela", {})
    noise = forensics.get("noise", {})
    comp  = forensics.get("compression", {})
    edge  = forensics.get("edge", {})
    exif  = forensics.get("exif", {})

    rows = [
        ("ELA Manipulation",  ela.get("manipulation_score", 0)),
        ("Noise Anomaly",     noise.get("noise_score", 0)),
        ("Compression",       comp.get("compression_score", 0)),
        ("Edge Consistency",  edge.get("edge_score", 0)),
        ("EXIF Anomaly",      exif.get("anomaly_score", 0)),
    ]

    rows_html = "".join([
        f'<div class="forensic-row"><span class="forensic-label">{lbl}</span>{chip(s)}</div>'
        for lbl, s in rows
    ])
    st.markdown(f'<div class="forensic-panel">{rows_html}</div>', unsafe_allow_html=True)


# ─── Feedback Widget ─────────────────────────────────────────

def render_feedback_widget(analysis_id: str):
    from database.db import save_feedback

    st.markdown(
        """
        <div class="feedback-panel">
          <div class="feedback-title">Was this analysis accurate?</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("Correct", key=f"fb_yes_{analysis_id}", use_container_width=True):
            save_feedback(analysis_id, is_correct=True)
            st.success("Feedback saved — thank you!")
            st.session_state.feedback_submitted = True
    with col2:
        if st.button("Incorrect", key=f"fb_no_{analysis_id}", use_container_width=True):
            save_feedback(analysis_id, is_correct=False)
            st.warning("Feedback noted — helps us improve!")
            st.session_state.feedback_submitted = True


# ─── Explainability Report (Phase 9) ─────────────────────────

def render_explainability_report(report: dict):
    """
    Render the full structured explainability report:
    Trust Score, Confidence, Reasoning Chain, Evidence, Risk Factors.
    """
    if not report:
        return

    section_header("Explainability Report", "Evidence · Confidence · Reasoning · Sources")

    # Top metrics row
    trust = int(clamp(report.get("trust_score", 0)))
    conf  = int(clamp(report.get("confidence", 0)))
    breakdown = report.get("claim_breakdown", {})
    dup = report.get("duplicate_claims_detected", 0)

    cols = st.columns(4)
    metrics = [
        ("Trust Score",    trust, "#00E5A0" if trust >= 60 else "#FFB800" if trust >= 35 else "#FF4560"),
        ("Confidence",     conf,  "#7C4DFF"),
        ("Claims Checked", breakdown.get("total", 0), "#00CFFF"),
        ("Duplicate Groups", dup, "#FFB800"),
    ]
    for col, (lbl, val, color) in zip(cols, metrics):
        with col:
            st.markdown(
                f'<div class="dash-kpi"><div class="dash-kpi-val" style="color:{color}">{val}</div>'
                f'<div class="dash-kpi-lbl">{lbl}</div></div>',
                unsafe_allow_html=True,
            )

    # Confidence basis
    if report.get("confidence_basis"):
        st.markdown(
            f"<div style='margin-top:10px;font-size:0.82rem;color:var(--tx-m);"
            f"padding:10px 14px;background:var(--card);border-radius:8px;"
            f"border:1px solid var(--border-s)'><strong style='color:var(--tx)'>Confidence basis:</strong> "
            f"{report['confidence_basis']}</div>",
            unsafe_allow_html=True,
        )

    # Evidence summary + sources
    sources = report.get("supporting_sources", [])
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    section_header("Supporting Sources", "")
    st.markdown(
        f"<div style='font-size:0.82rem;color:var(--tx-d);margin-bottom:8px'>"
        f"{report.get('evidence_summary', '')}</div>",
        unsafe_allow_html=True,
    )
    if sources:
        items = "".join([
            f'<div class="evidence-item"><span class="evidence-source">{s["source"]}</span>'
            f'<span class="evidence-title">{s["title"][:90]}</span>'
            f'<div style="font-size:0.75rem;color:var(--tx-d);margin-top:3px">'
            f'Relevance: {int(s["relevance"]*100)}% &middot; '
            f'<a href="{s["url"]}" target="_blank" style="color:var(--s)">{s["url"][:60]}…</a></div></div>'
            for s in sources
        ])
        st.markdown(f'<div class="evidence-panel">{items}</div>', unsafe_allow_html=True)


# ─── Evidence Panel (per-claim) ──────────────────────────────

def render_evidence_for_claims(evidence_map: dict):
    """Render retrieved evidence grouped by claim."""
    if not evidence_map:
        return
    section_header("Retrieved Evidence by Claim", "")
    for key, entry in list(evidence_map.items())[:5]:
        claim = entry.get("claim", "")
        evidence = entry.get("evidence", [])
        if not evidence:
            continue
        with st.expander(f"{claim[:90]}{'…' if len(claim) > 90 else ''}", expanded=False):
            for ev in evidence[:3]:
                st.markdown(
                    f'<div class="evidence-item"><span class="evidence-source">{ev.get("source","Web")}</span>'
                    f'<span class="evidence-title">{ev.get("title","Untitled")[:90]}</span>'
                    f'<div style="font-size:0.78rem;color:var(--tx-m);margin-top:4px">{ev.get("snippet","")[:200]}</div>'
                    f'<div style="font-size:0.73rem;color:var(--tx-d);margin-top:3px">'
                    f'Relevance: {int(ev.get("relevance",0)*100)}%</div></div>',
                    unsafe_allow_html=True,
                )


# ─── Claim Clusters (duplicate detection) ────────────────────

def render_claim_clusters(cluster_info: dict, claims: list):
    """Show duplicate / near-duplicate claim groups detected via embeddings."""
    if not cluster_info or cluster_info.get("duplicate_groups", 0) == 0:
        return
    section_header("Duplicate Claims Detected", "")
    for cluster in cluster_info.get("clusters", []):
        if len(cluster) < 2:
            continue
        items = "".join([
            f'<div style="padding:6px 0;font-size:0.83rem;color:var(--tx-m)">'
            f'&bull; {claims[i].get("claim","")[:120]}</div>'
            for i in cluster if i < len(claims)
        ])
        st.markdown(
            f'<div class="glass-card" style="border-color:rgba(255,184,0,0.2)">'
            f'<div style="font-size:0.74rem;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:0.08em;color:var(--yellow);margin-bottom:6px">'
            f'Similar Claims ({len(cluster)})</div>{items}</div>',
            unsafe_allow_html=True,
        )


# ─── Section Header ──────────────────────────────────────────

def section_header(title: str, sub: str = ""):
    sub_html = f"<span style='font-size:0.77rem;color:var(--tx-d);font-weight:400;margin-left:8px'>{sub}</span>" if sub else ""
    st.markdown(f'<div class="section-hdr">{title}{sub_html}</div>', unsafe_allow_html=True)


# ─── Info Banner ─────────────────────────────────────────────

def info_banner(title: str, body: str, icon: str = "ℹ"):
    st.markdown(
        f"""
        <div class="glass-card" style="border-color:rgba(0,207,255,0.18);">
          <div style="font-size:0.78rem;font-weight:700;text-transform:uppercase;
                      letter-spacing:0.09em;color:var(--s);margin-bottom:8px">{icon} {title}</div>
          <div style="font-size:0.87rem;color:var(--tx-m);line-height:1.65">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
