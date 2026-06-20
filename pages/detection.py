"""
TruthLens AI 2.0 — Detection Page
Full multi-agent analysis with deep reasoning, claim verification, and forensics.
"""
import streamlit as st
from PIL import Image
import io

from components.widgets import (
    render_verdict, score_bar, score_row,
    render_flags, render_findings, render_meta_flags,
    ai_explanation, info_banner, section_header,
    render_linguistic_scores, render_agent_trace,
    render_claim_cards, render_reasoning_chain,
    render_forensic_detail, render_feedback_widget,
    render_explainability_report, render_evidence_for_claims,
    render_claim_clusters,
)
from components.charts import make_gauge_chart, make_radar_chart, make_bar_chart
from components.footer import render_footer
from models.text_analyzer import run_text_analysis
from models.image_analyzer import run_image_analysis
from utils.config import GEMINI_API_KEY


def render_detection():
    st.markdown(
        """
        <div style="padding:36px 0 24px;text-align:center">
          <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.12em;
                      text-transform:uppercase;color:var(--p-light);margin-bottom:10px">
            AI Detection Suite
          </div>
          <div style="font-family:'Poppins',sans-serif;font-size:clamp(1.9rem,4vw,2.7rem);
                      font-weight:800;line-height:1.15;color:var(--tx);margin-bottom:14px">
            Analyze
            <span style="background:linear-gradient(135deg,#A67AFF,#00CFFF);
                         -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                         background-clip:text">Any Content</span>
          </div>
          <div style="font-size:0.93rem;color:var(--tx-m);max-width:600px;margin:0 auto">
            Multi-agent pipeline: claim extraction, evidence retrieval, fact-checking,
            risk assessment, and explainable AI reasoning.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not GEMINI_API_KEY:
        st.warning(
            "**Demo Mode** — No GEMINI_API_KEY found. "
            "Add it to your `.env` file to unlock live AI analysis.",
            icon="⚠️",
        )

    tab1, tab2 = st.tabs(["  Text & News Detection  ", "  Image & Deepfake Detection  "])

    with tab1:
        _fake_news_tab()

    with tab2:
        _deepfake_tab()


# ─── FAKE NEWS TAB ────────────────────────────────────────────

def _fake_news_tab():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    samples = {
        "Select a sample…": "",
        "NASA Webb Telescope (Credible)":
            "NASA confirms the James Webb Space Telescope has captured its first direct image "
            "of an exoplanet, marking a historic milestone according to the agency's official "
            "press release published on September 1, 2022.",
        "Health Misinformation":
            "BREAKING: Scientists CONFIRM drinking bleach cures cancer — Big Pharma is hiding "
            "this!! Share before they DELETE this!!! 100% natural cure discovered in Mexico.",
        "Political Propaganda":
            "The globalist deep state elites are using mainstream media to cover up the truth. "
            "Wake up sheeple! The economy has NEVER been worse. Crime is at record highs. "
            "Vote for change NOW before it is too late!",
        "Fabricated Statistic":
            "New study PROVES vaccines caused 500,000 deaths last year. The CDC and WHO are "
            "hiding this data from the public. Share this before they censor it. "
            "98% of hospitalized patients were vaccinated.",
    }

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    selected = st.selectbox("Quick sample (optional)", list(samples.keys()), key="sample_sel")
    user_text = st.text_area(
        "Paste text, headline, tweet, or article",
        value=samples[selected],
        height=160,
        placeholder="Paste a news headline, article, tweet, or any text content for analysis…",
        key="fn_text",
    )
    col_btn, col_hint, _ = st.columns([1.5, 3, 2])
    with col_btn:
        analyze = st.button("Run Analysis", key="analyze_text",  use_container_width=True)
    with col_hint:
        st.markdown(
            "<div style='padding-top:8px;font-size:0.78rem;color:var(--tx-d)'>"
            "6-agent pipeline · Claim extraction · Evidence retrieval · Fact-checking"
            "</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    if analyze and user_text.strip():
        with st.spinner("Running 6-agent analysis pipeline…"):
            result = run_text_analysis(user_text)
            st.session_state.text_result = result
            if "error" not in result:
                hist = st.session_state.setdefault("analysis_history", [])
                hist.append({
                    "label":      f"#{len(hist)+1}",
                    "fake_score": result.get("fake_score", 0),
                    "verdict":    result.get("verdict", ""),
                    "type":       "text",
                })

    result = st.session_state.get("text_result")
    if not result:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        info_banner(
            "HOW IT WORKS",
        "TruthLens v2.0 follows a six-agent verification workflow that extracts claims, retrieves evidence, fact-checks information, assesses risk, generates explainable reasoning, and delivers a final evidence-backed verdict. Unlike simple LLM wrappers, every verdict is grounded in evidence and verifiable signals.",
        )
        render_footer()
        return

    if "error" in result:
        st.error(result["error"])
        render_footer()
        return

    st.markdown("<hr style='border:none;border-top:1px solid rgba(124,77,255,0.14);margin:28px 0'>",
                unsafe_allow_html=True)

    # Agent trace
    if result.get("agent_trace"):
        render_agent_trace(result["agent_trace"])
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Verdict
    render_verdict(result.get("verdict", "UNCERTAIN"))
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Score KPI strip
    score_row(result)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Left/Right columns
    col_l, col_r = st.columns([1, 1])

    with col_l:
        section_header("Score Breakdown", "")
        score_bar("Fake Probability",    result.get("fake_score", 0),
                  "Probability content is fabricated")
        score_bar("Trust Score",         result.get("trust_score", 0),
                  "Overall credibility", invert=False)
        score_bar("Bias Score",          result.get("bias_score", 0),
                  "Editorial or political bias")
        score_bar("Manipulation Score",  result.get("manipulation_score", 0),
                  "Manipulative language detected")
        score_bar("AI Confidence",       result.get("confidence", 0),
                  "Confidence in this verdict")

        bias_dir = result.get("bias_direction", "")
        if bias_dir:
            st.markdown(
                f"<div style='margin-top:10px;padding:10px 16px;background:var(--card);"
                f"border-radius:8px;font-size:0.84rem;border:1px solid var(--border-s)'>"
                f"<span style='color:var(--tx-m)'>Bias Indicator:</span> "
                f"<strong style='color:var(--p-light)'>{bias_dir}</strong></div>",
                unsafe_allow_html=True,
            )

    with col_r:
        radar = {
            "Fake":         result.get("fake_score", 0),
            "Bias":         result.get("bias_score", 0),
            "Manipulation": result.get("manipulation_score", 0),
            "Distrust":     100 - result.get("trust_score", 100),
            "Confidence":   result.get("confidence", 0),
        }
        st.plotly_chart(make_radar_chart(radar), use_container_width=True)

    # Linguistic scores
    ling_scores = result.get("linguistic_scores", {})
    if ling_scores:
        section_header("Linguistic Analysis Signals", "")
        render_linguistic_scores(ling_scores)

    # AI reasoning chain
    if result.get("reasoning_chain"):
        render_reasoning_chain(result["reasoning_chain"])

    # AI explanation
    ai_explanation(result.get("explanation", ""))

    # Claim verification
    if result.get("claim_verification"):
        render_claim_cards(result["claim_verification"])

    # Duplicate claim clusters (embedding-based)
    if result.get("claim_clusters") and result.get("extracted_claims"):
        render_claim_clusters(result["claim_clusters"], result["extracted_claims"])

    # Retrieved evidence by claim
    if result.get("evidence_map"):
        render_evidence_for_claims(result["evidence_map"])

    # Red flags
    all_flags = result.get("red_flags", []) + result.get("risk_factors", [])
    if all_flags:
        render_flags(list(dict.fromkeys(all_flags))[:8])

    # Fact check summary
    fcs = result.get("fact_check_summary", "")
    if fcs:
        section_header("Fact-Check Summary", "")
        st.markdown(
            f"<div class='glass-card' style='border-color:rgba(0,229,160,0.2);"
            f"font-size:0.9rem;line-height:1.7;color:var(--tx-m)'>{fcs}</div>",
            unsafe_allow_html=True,
        )

    # Full explainability report (Phase 9)
    if result.get("explainability_report"):
        st.markdown("<hr style='border:none;border-top:1px solid rgba(124,77,255,0.14);margin:24px 0'>",
                    unsafe_allow_html=True)
        render_explainability_report(result["explainability_report"])

    # Gauges
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    with g1:
        st.plotly_chart(make_gauge_chart(result.get("confidence", 0),
                        "AI Confidence", "#7C4DFF"), use_container_width=True)
    with g2:
        st.plotly_chart(make_gauge_chart(result.get("fake_score", 0),
                        "Fake Score", "#FF4560"), use_container_width=True)

    # Feedback
    analysis_id = result.get("analysis_id", "unknown")
    if not st.session_state.get("feedback_submitted"):
        render_feedback_widget(analysis_id)

    render_footer()


# ─── DEEPFAKE TAB ─────────────────────────────────────────────

def _deepfake_tab():
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload an image for deepfake analysis",
        type=["jpg", "jpeg", "png", "webp"],
        key="df_upload",
        help="Supports JPG, PNG, WEBP up to 10 MB",
    )
    col_btn, col_hint, _ = st.columns([1.5, 3, 2])
    with col_btn:
        analyze = st.button("Analyze Image", key="analyze_img", use_container_width=True)
    with col_hint:
        st.markdown(
            "<div style='padding-top:8px;font-size:0.78rem;color:var(--tx-d)'>"
            "ELA · EXIF · Noise · Compression · Edge Analysis · AI Vision"
            "</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    if analyze and uploaded:
        with st.spinner("Running image forensics pipeline…"):
            result = run_image_analysis(uploaded)
            st.session_state.image_result = result
            if "error" not in result:
                hist = st.session_state.setdefault("analysis_history", [])
                hist.append({
                    "label":      f"#{len(hist)+1}",
                    "fake_score": result.get("ai_generated_score", 0),
                    "verdict":    result.get("verdict", ""),
                    "type":       "image",
                })

    result = st.session_state.get("image_result")
    if not result:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        info_banner(
            "Image Forensics Pipeline",
            "TruthLens v2.0 runs 5 independent forensic checks: "
            "(1) Error Level Analysis (ELA) detects re-saved/edited regions, "
            "(2) EXIF metadata checks for editing software and date tampering, "
            "(3) Noise analysis detects unnaturally smooth AI-generated textures, "
            "(4) Compression artifact analysis spots spliced regions, "
            "(5) Edge sharpness analysis finds inconsistent focus. "
            "All signals feed into an aggregate manipulation score alongside Gemini Vision AI.",
        )
        render_footer()
        return

    if "error" in result:
        st.error(result["error"])
        render_footer()
        return

    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(124,77,255,0.14);margin:28px 0'>",
        unsafe_allow_html=True,
    )

    render_verdict(result.get("verdict", "POSSIBLY MANIPULATED"))
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1])
    with col_l:
        if uploaded:
            try:
                uploaded.seek(0)
                img = Image.open(uploaded)
                st.image(img, caption="Uploaded Image", use_container_width=True)
            except Exception:
                pass

        # Image metadata
        st.markdown(
            f"""
            <div class="glass-card" style="margin-top:12px;font-size:0.84rem;line-height:2.1">
              <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                          letter-spacing:0.09em;color:var(--tx-m);margin-bottom:8px">File Metadata</div>
              <div><span style="color:var(--tx-d)">Dimensions:</span>
                   <strong style="color:var(--tx)">{result.get('image_size','N/A')}</strong></div>
              <div><span style="color:var(--tx-d)">Color Mode:</span>
                   <strong style="color:var(--tx)">{result.get('image_mode','N/A')}</strong></div>
              <div><span style="color:var(--tx-d)">File Size:</span>
                   <strong style="color:var(--tx)">{result.get('file_size','N/A')}</strong></div>
              <div><span style="color:var(--tx-d)">Format:</span>
                   <strong style="color:var(--tx)">{result.get('format','N/A')}</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # EXIF metadata
        exif_meta = result.get("exif_metadata", {})
        if exif_meta:
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            section_header("EXIF Data", "")
            rows = "".join([
                f"<div class='forensic-row'><span class='forensic-label'>{k}</span>"
                f"<span class='forensic-val' style='color:var(--tx-m);font-size:0.78rem'>{v}</span></div>"
                for k, v in list(exif_meta.items())[:8]
            ])
            st.markdown(f'<div class="forensic-panel">{rows}</div>', unsafe_allow_html=True)

    with col_r:
        section_header("Authenticity Scores", "")
        score_bar("AI Generated Probability", result.get("ai_generated_score", 0),
                  "Likelihood of AI generation")
        score_bar("Manipulation Score",        result.get("manipulation_score", 0),
                  "Signs of pixel-level tampering")
        score_bar("Authenticity Score",         result.get("authenticity_score", 0),
                  "Probability of authentic origin", invert=False)
        score_bar("Analysis Confidence",        result.get("confidence", 0),
                  "Confidence in this analysis")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        g1, g2 = st.columns(2)
        with g1:
            st.plotly_chart(make_gauge_chart(result.get("ai_generated_score", 0),
                            "AI Generated", "#8B5CF6"), use_container_width=True)
        with g2:
            st.plotly_chart(make_gauge_chart(result.get("manipulation_score", 0),
                            "Manipulation", "#FF4560"), use_container_width=True)

    # Forensic detail breakdown
    if result.get("forensic_detail"):
        render_forensic_detail(result["forensic_detail"])

    # AI explanation
    ai_explanation(result.get("explanation", ""))

    # Findings
    if result.get("findings"):
        render_findings(result["findings"])

    # Metadata flags
    if result.get("metadata_flags"):
        render_meta_flags(result["metadata_flags"])

    # Explainability report
    if result.get("explainability_report"):
        st.markdown("<hr style='border:none;border-top:1px solid rgba(124,77,255,0.14);margin:24px 0'>",
                    unsafe_allow_html=True)
        render_explainability_report(result["explainability_report"])

    # Feedback
    analysis_id = result.get("analysis_id", "img_unknown")
    render_feedback_widget(analysis_id)

    render_footer()
