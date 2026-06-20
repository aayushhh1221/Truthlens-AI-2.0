"""
TruthLens AI 2.0 — Document & Credential Verification Page
OCR + Template Matching + Forgery Detection for certificates, IDs, academic documents.
"""
import streamlit as st
from PIL import Image

from components.widgets import (
    render_verdict, score_bar, info_banner, section_header,
    render_flags, render_feedback_widget,
)
from components.footer import render_footer
from models.document_analyzer import run_document_verification
from utils.config import GEMINI_API_KEY


def render_document_verify():
    st.markdown(
        """
        <div style="padding:36px 0 24px;text-align:center">
          <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.12em;
                      text-transform:uppercase;color:var(--p-light);margin-bottom:10px">
            Document Intelligence
          </div>
          <div style="font-family:'Poppins',sans-serif;font-size:clamp(1.9rem,4vw,2.7rem);
                      font-weight:800;line-height:1.15;color:var(--tx);margin-bottom:14px">
            Credential &amp;
            <span style="background:linear-gradient(135deg,#A67AFF,#00CFFF);
                         -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                         background-clip:text">Document Verification</span>
          </div>
          <div style="font-size:0.93rem;color:var(--tx-m);max-width:640px;margin:0 auto">
            Upload certificates, ID cards, or academic documents. TruthLens runs OCR,
            template-structure analysis, date/font consistency checks, and AI-powered
            forgery detection.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not GEMINI_API_KEY:
        st.warning(
            "**Demo Mode** — No GEMINI_API_KEY found. Add it to your `.env` file "
            "to unlock live AI-powered forgery detection.",
            icon="⚠️",
        )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload a document (Certificate, ID Card, Degree, PDF)",
        type=["pdf", "png", "jpg", "jpeg"],
        key="doc_upload",
        help="Supports PDF, JPG, PNG up to 10 MB",
    )
    col_btn, col_hint, _ = st.columns([1.5, 3, 2])
    with col_btn:
        analyze = st.button("Verify Document", key="analyze_doc",  use_container_width=True)
    with col_hint:
        st.markdown(
            "<div style='padding-top:8px;font-size:0.78rem;color:var(--tx-d)'>"
            "OCR · Template Matching · Date Consistency · AI Forgery Detection"
            "</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    if analyze and uploaded:
        with st.spinner("Running document forensics pipeline…"):
            result = run_document_verification(uploaded)
            st.session_state.doc_result = result
            if "error" not in result:
                hist = st.session_state.setdefault("analysis_history", [])
                hist.append({
                    "label":      f"#{len(hist)+1}",
                    "fake_score": result.get("forgery_score", 0),
                    "verdict":    result.get("verdict", ""),
                    "type":       "document",
                })

    result = st.session_state.get("doc_result")
    if not result:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        info_banner(
            "Document Verification Pipeline",
            "TruthLens v2.0 verifies certificates, academic degrees, ID cards, and financial documents through an AI-powered forensic workflow. The system extracts visible text, identifies the document type, validates required fields, analyzes font and date consistency, and uses Gemini Vision AI to detect potential forgery signals. The result is a comprehensive authenticity assessment with confidence scores and detailed forgery indicators.",
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

    # Doc type badge
    doc_type_display = result.get("doc_type", "general_document").replace("_", " ").title()
    st.markdown(f'<div class="doc-type-badge">{doc_type_display}</div>', unsafe_allow_html=True)

    render_verdict(result.get("verdict", "INCONCLUSIVE"))
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1])

    with col_l:
        if uploaded and uploaded.type != "application/pdf":
            try:
                uploaded.seek(0)
                img = Image.open(uploaded)
                st.image(img, caption="Uploaded Document", use_container_width=True)
            except Exception:
                pass
        elif uploaded:
            st.markdown(
                f"""
                <div class="glass-card" style="text-align:center;padding:40px 20px">
                  <div style="font-size:0.9rem;color:var(--tx-m)">PDF Document</div>
                  <div style="font-size:0.78rem;color:var(--tx-d);margin-top:6px">{uploaded.name}</div>
                  <div style="font-size:0.78rem;color:var(--tx-d)">{result.get('file_size','')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Template field completeness
        template = result.get("template_analysis", {})
        if template.get("expected_fields"):
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            section_header("Template Field Completeness", "")
            found_set = set(template.get("found_fields", []))
            rows = ""
            for field in template.get("expected_fields", []):
                is_found = field in found_set
                icon  = "&#10003;" if is_found else "&#10007;"
                cls   = "field-found" if is_found else "field-missing"
                rows += (
                    f'<div class="template-field-row">'
                    f'<span class="field-name">{field.title()}</span>'
                    f'<span class="{cls}">{icon}</span></div>'
                )
            st.markdown(f'<div class="forensic-panel">{rows}</div>', unsafe_allow_html=True)
            st.markdown(
                f"<div style='margin-top:8px;font-size:0.8rem;color:var(--tx-d)'>"
                f"Completeness: <strong style='color:var(--tx)'>{template.get('completeness',0)}%</strong></div>",
                unsafe_allow_html=True,
            )

    with col_r:
        section_header("Authenticity Scores", "")
        score_bar("Authenticity Score", result.get("authenticity_score", 0),
                  "Probability document is genuine")
        score_bar("Forgery Score",      result.get("forgery_score", 0),
                  "Probability of forgery / tampering")
        score_bar("AI Confidence",      result.get("confidence", 0),
                  "Confidence in this verdict")

        # OCR preview
        ocr_text = result.get("ocr_text", "")
        if ocr_text and not ocr_text.startswith("["):
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            section_header("Extracted Text (OCR)", "")
            preview = ocr_text[:600] + ("…" if len(ocr_text) > 600 else "")
            st.markdown(
                f"<div class='glass-card' style='font-size:0.8rem;line-height:1.7;"
                f"color:var(--tx-m);max-height:220px;overflow-y:auto;white-space:pre-wrap'>{preview}</div>",
                unsafe_allow_html=True,
            )
        elif ocr_text.startswith("["):
            st.markdown(
                f"<div style='margin-top:10px;font-size:0.78rem;color:var(--tx-d)'>{ocr_text}</div>",
                unsafe_allow_html=True,
            )

    # AI Explanation
    if result.get("explanation"):
        section_header("AI Forensic Analysis", "")
        st.markdown(
            f"""
            <div class="ai-box">
              <div class="ai-box-lbl">Reasoning</div>
              {result['explanation']}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Forgery indicators
    if result.get("forgery_indicators"):
        render_flags(result["forgery_indicators"], "Forgery Indicators")

    # Authenticity signals
    if result.get("authenticity_signals"):
        section_header("Authenticity Signals", "")
        for s in result["authenticity_signals"][:6]:
            st.markdown(
                f'<div class="meta-item">{s}</div>', unsafe_allow_html=True,
            )

    # Recommendation
    if result.get("recommendation"):
        st.markdown(
            f"""
            <div class="glass-card" style="border-color:rgba(0,229,160,0.2);margin-top:14px">
              <div style="font-size:0.69rem;font-weight:700;letter-spacing:0.1em;
                          text-transform:uppercase;color:var(--green);margin-bottom:8px">Recommendation</div>
              <div style="font-size:0.88rem;color:var(--tx-m);line-height:1.65">{result['recommendation']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Feedback
    doc_id = result.get("doc_id", "doc_unknown")
    render_feedback_widget(doc_id)

    render_footer()
