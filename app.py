"""
app.py
------
Entry point for the EEG Frequency Band Analyzer Streamlit app.
Run with:  streamlit run app.py
"""

import streamlit as st
from ui.theme import inject_theme
from utils.state import init_state

st.set_page_config(
    page_title="EEG Frequency Band Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_state()
inject_theme()

from ui.pages import (
    home,
    upload,
    raw_eeg,
    filtering,
    psd,
    ica,
    freq_bands,
    sensor_map,
    download,
    settings,
)

NAV_ITEMS = [
    ("🏠 Home", home),
    ("📂 Upload EEG", upload),
    ("📈 Raw EEG", raw_eeg),
    ("🎚 Filtering", filtering),
    ("📊 PSD Analysis", psd),
    ("🧠 ICA", ica),
    ("🌈 Frequency Bands", freq_bands),
    ("🗺 Sensor Map", sensor_map),
    ("⬇ Download", download),
    ("⚙ Settings", settings),
]
LABELS = [label for label, _ in NAV_ITEMS]
PAGES = {label: module for label, module in NAV_ITEMS}

with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding: 0.5rem 0 1.2rem 0;">
            <div style="font-size:2rem;">🧠</div>
            <div style="font-weight:800; font-size:1.15rem; color:#E8ECF4;">EEG Analyzer</div>
            <div style="font-size:0.75rem; color:#9AA4B8; letter-spacing:0.05em;">FREQUENCY BAND SUITE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    default_index = 0
    if st.session_state.get("_nav_override"):
        default_index = LABELS.index(st.session_state.pop("_nav_override"))

    selected_label = st.radio(
        "Navigate",
        LABELS,
        index=default_index,
        label_visibility="collapsed",
        key="_nav_radio",
    )

    st.divider()
    if st.session_state.get("raw") is not None:
        st.success(f"✅ Data loaded\n\n**{st.session_state.get('source_filename', 'Unknown')}**")
    else:
        st.info("No EEG data loaded yet.")

    st.caption("v1.0 · Streamlit + MNE-Python + Plotly")

PAGES[selected_label].render()
