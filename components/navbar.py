"""
TruthLens AI 2.0 — Navbar Component
"""
import streamlit as st

NAV_ITEMS = ["Home", "Detection", "Forensics", "Analytics", "Dashboard", "About"]


def render_navbar():
    st.markdown(
        '<div class="nav-marker" style="display:none"></div>',
        unsafe_allow_html=True
    )

    col_brand, *nav_cols, col_space = st.columns(
    [2.5, 1.0, 1.2, 1.2, 1.2, 1.5, 1.0, 0.5]
)

    with col_brand:
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:10px;padding:12px 0 8px;">
              <div style="width:32px;height:32px;background:linear-gradient(135deg,#7C4DFF,#00CFFF);
                          border-radius:8px;display:flex;align-items:center;justify-content:center;
                          font-size:15px;font-weight:900;color:#fff;font-family:'Poppins',sans-serif;">T</div>
              <span style="font-family:'Poppins',sans-serif;font-weight:800;font-size:1.05rem;
                           background:linear-gradient(135deg,#A67AFF,#00CFFF);
                           -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                           background-clip:text;">TruthLens AI</span>
              <span style="font-size:0.6rem;font-weight:700;color:#7C4DFF;letter-spacing:0.08em;
                           background:rgba(124,77,255,0.12);border:1px solid rgba(124,77,255,0.25);
                           padding:2px 7px;border-radius:4px;">v2.0</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    current = st.session_state.get("page", "Home")

    for col, label in zip(nav_cols, NAV_ITEMS):
        with col:
            if current == label:
                st.markdown(
                    f'<div class="nav-active-item">{label}</div>',
                    unsafe_allow_html=True,
                )
            else:
                if st.button(
                    label,
                    key=f"nav_{label}",
                    use_container_width=True,
                ):
                    st.session_state.page = label
                    st.rerun()

    # Separator
    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(124,77,255,0.14);margin:0 0 0;'>",
        unsafe_allow_html=True,
    )