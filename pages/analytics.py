"""TruthLens AI 2.0 — Session Analytics."""
import streamlit as st
from components.charts import (
    make_gauge_chart, make_radar_chart, make_bar_chart, make_history_line_chart,
)
from components.widgets import section_header, info_banner
from components.footer import render_footer
from utils.helpers import get_risk_color


def render_analytics():
    st.markdown(
        """
        <div style="padding:36px 0 24px;text-align:center">
          <div class="section-label">Insights</div>
          <div class="section-title">Session <span class="grad-text">Analytics</span></div>
          <div class="section-subtitle" style="margin-bottom:0">
            Visual intelligence from every analysis run in this session.
            For platform-wide statistics, see the Dashboard.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    text_result  = st.session_state.get("text_result")
    image_result = st.session_state.get("image_result")
    doc_result   = st.session_state.get("doc_result")
    history      = st.session_state.get("analysis_history", [])

    if not text_result and not image_result and not doc_result:
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        info_banner(
            "No data yet",
            "Run a Text, Image, or Document analysis first, then return here to see "
            "your session analytics, charts, and statistics. For aggregated "
            "platform-wide metrics across all users, visit the Dashboard page.",
            "&#128202;",
        )
        render_footer()
        return

    # ── KPI row ──────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    total    = len(history)
    flagged  = sum(1 for h in history if any(
        kw in h.get("verdict", "").upper()
        for kw in ["FAKE", "GENERATED", "DEEPFAKE", "MANIPULATED", "FORGED"]
    ))
    avg_risk = int(sum(h.get("fake_score", 0) for h in history) / total) if total else 0
    txt_cnt  = sum(1 for h in history if h.get("type") == "text")
    img_cnt  = sum(1 for h in history if h.get("type") == "image")
    doc_cnt  = sum(1 for h in history if h.get("type") == "document")

    kpis = [
        ("Analyses Run",   str(total),                    "#7C4DFF"),
        ("Flagged",        str(flagged),                  "#FF4560"),
        ("Avg Risk Score", f"{avg_risk}%",                get_risk_color(avg_risk)),
        ("Text/Img/Doc",   f"{txt_cnt}/{img_cnt}/{doc_cnt}", "#00CFFF"),
    ]
    for col, (lbl, val, color) in zip([k1, k2, k3, k4], kpis):
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

    st.markdown("<hr class='section-divider' style='margin:28px 0'>", unsafe_allow_html=True)

    # ── Text analysis charts ─────────────────────────────────
    if text_result and "error" not in text_result:
        section_header("Text & Misinformation Analysis", "")
        col1, col2 = st.columns([1, 1])

        with col1:
            labels = ["Fake Score", "Bias Score", "Manipulation", "Distrust"]
            values = [
                text_result.get("fake_score", 0),
                text_result.get("bias_score", 0),
                text_result.get("manipulation_score", 0),
                100 - text_result.get("trust_score", 0),
            ]
            st.plotly_chart(make_bar_chart(labels, values, "Risk Factor Breakdown"), use_container_width=True)

        with col2:
            ling = text_result.get("linguistic_scores", {})
            if ling:
                labels2 = ["Clickbait", "Emotional", "Urgency", "Propaganda", "Certainty"]
                values2 = [
                    ling.get("clickbait", 0), ling.get("emotional", 0),
                    ling.get("urgency", 0), ling.get("propaganda", 0),
                    ling.get("certainty", 0),
                ]
                st.plotly_chart(make_bar_chart(labels2, values2, "Linguistic Signal Breakdown"), use_container_width=True)
            else:
                radar = {
                    "Fake":         text_result.get("fake_score", 0),
                    "Bias":         text_result.get("bias_score", 0),
                    "Manipulation": text_result.get("manipulation_score", 0),
                    "Distrust":     100 - text_result.get("trust_score", 0),
                    "Confidence":   text_result.get("confidence", 0),
                }
                st.plotly_chart(make_radar_chart(radar), use_container_width=True)

        # Claim verification stats
        claim_stats = text_result.get("claim_stats", {})
        if claim_stats.get("total", 0) > 0:
            cs1, cs2, cs3, cs4 = st.columns(4)
            for col, (lbl, val) in zip([cs1, cs2, cs3, cs4], [
                ("Total Claims",  claim_stats.get("total", 0)),
                ("Supported",     claim_stats.get("supported", 0)),
                ("Contradicted",  claim_stats.get("contradicted", 0)),
                ("Unverified",    claim_stats.get("unverified", 0)),
            ]):
                with col:
                    st.markdown(
                        f'<div class="dash-kpi"><div class="dash-kpi-val" style="color:#00CFFF;font-size:1.6rem">{val}</div>'
                        f'<div class="dash-kpi-lbl">{lbl}</div></div>',
                        unsafe_allow_html=True,
                    )

        g1, g2 = st.columns(2)
        with g1:
            st.plotly_chart(make_gauge_chart(text_result.get("confidence", 0), "AI Confidence", "#7C4DFF"), use_container_width=True)
        with g2:
            st.plotly_chart(make_gauge_chart(text_result.get("fake_score", 0), "Fake Score", "#FF4560"), use_container_width=True)

    # ── Image analysis charts ────────────────────────────────
    if image_result and "error" not in image_result:
        st.markdown("<hr class='section-divider' style='margin:28px 0'>", unsafe_allow_html=True)
        section_header("Image & Deepfake Analysis", "")
        g1, g2, g3 = st.columns(3)
        with g1:
            st.plotly_chart(make_gauge_chart(image_result.get("ai_generated_score", 0), "AI Generated", "#8B5CF6"), use_container_width=True)
        with g2:
            st.plotly_chart(make_gauge_chart(image_result.get("manipulation_score", 0), "Manipulation", "#FF4560"), use_container_width=True)
        with g3:
            st.plotly_chart(make_gauge_chart(image_result.get("authenticity_score", 0), "Authenticity", "#00E5A0"), use_container_width=True)

        forensic = image_result.get("forensic_detail", {})
        if forensic:
            labels = ["ELA", "Noise", "Compression", "Edge", "EXIF"]
            values = [
                forensic.get("ela", {}).get("manipulation_score", 0),
                forensic.get("noise", {}).get("noise_score", 0),
                forensic.get("compression", {}).get("compression_score", 0),
                forensic.get("edge", {}).get("edge_score", 0),
                forensic.get("exif", {}).get("anomaly_score", 0),
            ]
            st.plotly_chart(make_bar_chart(labels, values, "Forensic Signal Breakdown"), use_container_width=True)

    # ── Document analysis ────────────────────────────────────
    if doc_result and "error" not in doc_result:
        st.markdown("<hr class='section-divider' style='margin:28px 0'>", unsafe_allow_html=True)
        section_header("Document Verification Analysis", "")
        g1, g2 = st.columns(2)
        with g1:
            st.plotly_chart(make_gauge_chart(doc_result.get("authenticity_score", 0), "Authenticity", "#00E5A0"), use_container_width=True)
        with g2:
            st.plotly_chart(make_gauge_chart(doc_result.get("forgery_score", 0), "Forgery Risk", "#FF4560"), use_container_width=True)

        template = doc_result.get("template_analysis", {})
        if template:
            st.markdown(
                f"<div class='glass-card'>Template completeness: "
                f"<strong style='color:var(--p-light)'>{template.get('completeness', 0)}%</strong> "
                f"&mdash; {len(template.get('found_fields', []))} of "
                f"{len(template.get('expected_fields', []))} expected fields found.</div>",
                unsafe_allow_html=True,
            )

    # ── History line chart ───────────────────────────────────
    if len(history) > 1:
        st.markdown("<hr class='section-divider' style='margin:28px 0'>", unsafe_allow_html=True)
        section_header("Session History — Risk Score Trend", "")
        fig = make_history_line_chart(history)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    # ── Clear button ─────────────────────────────────────────
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([3, 1, 3])
    with btn_col:
        if st.button("Clear Session Data", key="clear_dash", use_container_width=True):
            st.session_state.analysis_history = []
            st.session_state.text_result = None
            st.session_state.image_result = None
            st.session_state.doc_result = None
            st.session_state.feedback_submitted = False
            st.rerun()

    render_footer()
