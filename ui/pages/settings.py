import streamlit as st
from ui.components import footer
from utils.state import reset_all
from utils.backend_bridge import DEBUG_LOG


def render():
    st.title("⚙ Settings")

    st.markdown("#### Session")
    if st.button("🗑 Reset session (clear loaded data)"):
        reset_all()
        st.success("Session cleared.")
        st.rerun()

    st.markdown("#### Backend Integration Status")
    st.caption(
        "This shows whether your real `data/*.py` functions were found, or whether "
        "the built-in fallback ran instead. See `utils/backend_bridge.py` to wire in "
        "your exact function names."
    )
    if DEBUG_LOG:
        for line in DEBUG_LOG:
            st.text(line)
    else:
        st.text("No backend calls made yet this session.")

    st.markdown("#### About")
    st.write(
        "EEG Frequency Band Analyzer — a Streamlit + MNE-Python + Plotly dashboard "
        "for EEG signal exploration and frequency-band feature extraction."
    )

    footer()
