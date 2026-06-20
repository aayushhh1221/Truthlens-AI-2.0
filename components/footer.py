"""TruthLens AI — Site Footer. Enterprise-grade readability."""
import streamlit as st


def render_footer():
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("<div class='footer-wrap'>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.5, 1, 1])

    with c1:
        st.markdown(
            """
            <div class="footer-brand-name">TruthLens AI</div>
            <div class="footer-brand-desc">
                Fighting misinformation and synthetic media with advanced AI
                detection technology. Built with purpose by Team HackManthan.
            </div>
            <div class="footer-contact">
                <div>contact@truthlens.ai</div>
                <div>DDUGU, Gorakhpur, India</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="footer-heading">Quick Links</div>
            <div class="footer-link-item">Home</div>
            <div class="footer-link-item">Detection</div>
            <div class="footer-link-item">Documents</div>
            <div class="footer-link-item">Analytics</div>
            <div class="footer-link-item">Dashboard</div>
            <div class="footer-link-item">About</div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="footer-heading">Technology</div>
            <div class="footer-link-item">Google Gemini 2.0</div>
            <div class="footer-link-item">Multi-Agent RAG Pipeline</div>
            <div class="footer-link-item">Sentence Transformers</div>
            <div class="footer-link-item">SQLite + Streamlit</div>
            <div class="footer-link-item">Plotly</div>
            <div class="footer-link-item">Pillow + SciPy</div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="footer-bottom">
            <div class="footer-copy">
                &copy; 2026 TruthLens AI &mdash; Built to fight misinformation
            </div>
            <div class="footer-team">Team HackManthan &nbsp;&middot;&nbsp; DDUGU Gorakhpur</div>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )