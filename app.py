"""
TruthLens AI 2.0 — Main Application Entry Point
Multi-Agent Misinformation & Deepfake Detection Platform

Run with: streamlit run app.py
"""

import streamlit as st
import uuid


#st.write("APP STARTED")

# ── Page config (must be first Streamlit call) ─────────────────
st.set_page_config(
    page_title="TruthLens AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Core imports ───────────────────────────────────────────────
from styles.design_system import CSS
from components.navbar import render_navbar
from pages.home import render_home
from pages.detection import render_detection
from pages.document_verify import render_document_verify
from pages.analytics import render_analytics
from pages.dashboard import render_dashboard
from pages.about import render_about
from database.db import init_database, get_or_create_user
from analytics.continuous_learning import ensure_baseline_version

# ── Initialize database ───────────────────────────────────────
init_database()
ensure_baseline_version()

# ── Inject global CSS ─────────────────────────────────────────
st.markdown(CSS, unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────
defaults = {
    "page": "Home",
    "text_result": None,
    "image_result": None,
    "doc_result": None,
    "analysis_history": [],
    "feedback_submitted": False,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Track session as a "user" row ──────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
get_or_create_user(st.session_state.session_id)

# ── Render navbar ─────────────────────────────────────────────
render_navbar()

# ── Route to page ─────────────────────────────────────────────
page = st.session_state.page

if page == "Home":
    render_home()
elif page == "Detection":
    render_detection()
elif page == "Forensics":
    render_document_verify()
elif page == "Analytics":
    render_analytics()
elif page == "Dashboard":
    render_dashboard()
elif page == "About":
    render_about()
else:
    st.session_state.page = "Home"
    st.rerun()
