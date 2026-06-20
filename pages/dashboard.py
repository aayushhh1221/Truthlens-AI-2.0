"""
TruthLens AI 2.0 — Professional Dashboard
Total analyses, fake content detected, document verifications, feedback accuracy,
learning progress, model performance.
"""
import streamlit as st
from components.footer import render_footer
from components.widgets import section_header, info_banner
from components.charts import make_daily_trend_chart, make_donut_chart
from database.db import get_analyses_stats, get_daily_counts, get_user_count
from analytics.continuous_learning import (
    compute_retraining_readiness, get_model_versions,
    ensure_baseline_version, suggest_threshold_adjustment,
)
from utils.helpers import get_risk_color


def render_dashboard():
    st.markdown(
        """
        <div style="padding:36px 0 24px;text-align:center">
          <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.12em;
                      text-transform:uppercase;color:var(--p-light);margin-bottom:10px">
            Platform Intelligence
          </div>
          <div style="font-family:'Poppins',sans-serif;font-size:clamp(1.9rem,4vw,2.7rem);
                      font-weight:800;line-height:1.15;color:var(--tx);margin-bottom:14px">
            System
            <span style="background:linear-gradient(135deg,#A67AFF,#00CFFF);
                         -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                         background-clip:text">Dashboard</span>
          </div>
          <div style="font-size:0.93rem;color:var(--tx-m);max-width:600px;margin:0 auto">
            Real-time platform statistics, model performance, and continuous learning progress.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stats = get_analyses_stats()
    daily = get_daily_counts(30)
    user_count = get_user_count()

    if stats["total"] == 0:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        info_banner(
            "No Data Yet",
            "Run some analyses on the Detection or Documents pages — every result is "
            "stored in the local database and will appear here with full statistics.",
        )
        render_footer()
        return

    # ── Top KPI Row ─────────────────────────────────────────
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    kpis = [
        ("Total Analyses",     stats["total"],   "#7C4DFF"),
        ("Fake/High-Risk",     stats["fake"],    "#FF4560"),
        ("Document Checks",    stats["docs"],    "#00CFFF"),
        ("Feedback Collected", stats["fb_total"],"#FFB800"),
        ("Feedback Accuracy",  f'{stats["accuracy"]}%', "#00E5A0"),
        ("Sessions",           user_count,       "#A67AFF"),
    ]
    for col, (lbl, val, color) in zip([k1, k2, k3, k4, k5, k6], kpis):
        with col:
            st.markdown(
                f"""
                <div class="dash-kpi">
                  <div class="dash-kpi-val" style="color:{color}">{val}</div>
                  <div class="dash-kpi-lbl">{lbl}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<hr style='border:none;border-top:1px solid rgba(124,77,255,0.14);margin:28px 0'>",
                unsafe_allow_html=True)

    # ── Content Type Distribution + Daily Trend ─────────────
    col_a, col_b = st.columns([1, 2])

    with col_a:
        section_header("Content Type Distribution", "")
        labels = ["Text", "Image", "Document"]
        values = [stats["texts"], stats["images"], stats["docs"]]
        fig = make_donut_chart(labels, values, colors=["#7C4DFF", "#00CFFF", "#00E5A0"])
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(
                "<div class='glass-card' style='text-align:center;color:var(--tx-d)'>"
                "Not enough data yet.</div>", unsafe_allow_html=True)

    with col_b:
        section_header("Analyses Over Time (30 days)", "")
        fig = make_daily_trend_chart(daily)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(
                "<div class='glass-card' style='text-align:center;color:var(--tx-d)'>"
                "Not enough historical data yet — check back after more analyses.</div>",
                unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid rgba(124,77,255,0.14);margin:28px 0'>",
                unsafe_allow_html=True)

    # ── Continuous Learning Progress ────────────────────────
    ensure_baseline_version()
    section_header("Continuous Learning Progress", "")
    readiness = compute_retraining_readiness(target_samples=100)
    fb_total  = readiness["total_samples"]
    accuracy  = stats["accuracy"]
    progress_pct = readiness["progress_pct"]
    learning_target = readiness["target_samples"]

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f"""
            <div class="glass-card">
              <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                <span style="font-size:0.85rem;color:var(--tx-m);font-weight:600">
                  Feedback Samples Collected: {fb_total} / {learning_target}
                </span>
                <span style="font-size:0.85rem;color:var(--p-light);font-weight:700">{progress_pct}%</span>
              </div>
              <div class="learning-bar"><div class="learning-fill" style="width:{progress_pct}%"></div></div>
              <div style="font-size:0.78rem;color:var(--tx-d);margin-top:10px;line-height:1.6">
                Each "Correct" / "Incorrect" submission is stored and used to evaluate model
                performance. Once {learning_target} samples are collected, a recalibration cycle
                is recommended to fine-tune the linguistic risk thresholds.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Threshold recalibration suggestions
        suggestion = suggest_threshold_adjustment()
        if suggestion.get("has_recommendation"):
            recs = "".join([f"<li style='margin-bottom:4px'>{r}</li>" for r in suggestion["recommendations"]])
            st.markdown(
                f"""
                <div class="glass-card" style="margin-top:10px;border-color:rgba(255,184,0,0.2)">
                  <div style="font-size:0.74rem;font-weight:700;text-transform:uppercase;
                              letter-spacing:0.08em;color:var(--yellow);margin-bottom:8px">
                    Recalibration Suggested
                  </div>
                  <ul style="font-size:0.82rem;color:var(--tx-m);padding-left:18px;margin:0">{recs}</ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif fb_total >= 10:
            st.markdown(
                "<div class='glass-card' style='margin-top:10px;border-color:rgba(0,229,160,0.2)'>"
                "<div style='font-size:0.82rem;color:var(--tx-m)'>"
                "No threshold recalibration needed — current scoring thresholds align "
                "well with user feedback.</div></div>",
                unsafe_allow_html=True,
            )

    with col2:
        acc_color = get_risk_color(100 - accuracy) if fb_total else "#5B6A9A"
        st.markdown(
            f"""
            <div class="dash-kpi" style="height:100%">
              <div class="dash-kpi-val" style="color:{acc_color}">{accuracy}%</div>
              <div class="dash-kpi-lbl">User-Reported Accuracy</div>
              <div style="font-size:0.74rem;color:var(--tx-d);margin-top:8px">
                {readiness['correct']} correct of {fb_total} rated
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='border:none;border-top:1px solid rgba(124,77,255,0.14);margin:28px 0'>",
                unsafe_allow_html=True)

    # ── Model Versioning / Performance ──────────────────────
    section_header("Model Versions & Pipeline Status", "")
    versions = get_model_versions()
    mv1, mv2, mv3 = st.columns(3)
    pipeline_cards = [
        ("Multi-Agent Pipeline", "Active",
         "6-agent orchestration: claim extraction, RAG evidence retrieval, fact-checking, "
         "risk assessment, explainability, final judging."),
        ("Text Forensics Engine", "Active",
         "Rule-based linguistic analysis (clickbait, emotional tone, urgency, propaganda, "
         "credibility) plus embedding-based semantic similarity to known misinformation."),
        ("Image Forensics Engine", "Active",
         "ELA, EXIF, noise, compression, and edge analysis combined with Gemini Vision AI "
         "for deepfake and manipulation detection."),
    ]
    for col, (title, status, desc) in zip([mv1, mv2, mv3], pipeline_cards):
        with col:
            st.markdown(
                f"""
                <div class="info-card" style="height:100%">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
                    <div class="info-card-title">{title}</div>
                    <span style="font-size:0.66rem;font-weight:700;letter-spacing:0.08em;
                                 text-transform:uppercase;color:var(--green);
                                 background:rgba(0,229,160,0.12);border:1px solid rgba(0,229,160,0.25);
                                 padding:2px 8px;border-radius:4px;white-space:nowrap">{status}</span>
                  </div>
                  <div class="info-card-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if versions:
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        rows_html = ""
        for v in versions[:5]:
            acc = v.get("accuracy") or 0
            rows_html += (
                f'<div class="forensic-row">'
                f'<span class="forensic-label">{v["version"]} — {v.get("notes","")[:80]}</span>'
                f'<span style="display:flex;align-items:center;gap:10px">'
                f'<span style="font-size:0.78rem;color:var(--tx-d)">{(v.get("created_at") or "")[:19]}</span>'
                f'<span class="forensic-score-chip chip-low">{acc:.1f}% acc</span>'
                f'</span></div>'
            )
        st.markdown(f'<div class="forensic-panel">{rows_html}</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid rgba(124,77,255,0.14);margin:28px 0'>",
                unsafe_allow_html=True)

    # ── Recent Analyses Table ────────────────────────────────
    section_header("Recent Analyses", "")
    recent = stats.get("recent", [])
    if recent:
        rows_html = ""
        for r in recent[:10]:
            score = r.get("fake_score") or 0
            color = get_risk_color(int(score))
            verdict = r.get("verdict", "—")
            rtype   = (r.get("type") or "—").title()
            created = (r.get("created_at") or "")[:19]
            rows_html += (
                f'<div class="forensic-row">'
                f'<span class="forensic-label">{rtype} · {verdict}</span>'
                f'<span style="display:flex;align-items:center;gap:10px">'
                f'<span style="font-size:0.78rem;color:var(--tx-d)">{created}</span>'
                f'<span class="forensic-score-chip" style="background:{color}22;color:{color}">{int(score)}</span>'
                f'</span></div>'
            )
        st.markdown(f'<div class="forensic-panel">{rows_html}</div>', unsafe_allow_html=True)

    render_footer()
