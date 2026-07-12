import streamlit as st
from ui.components import hero, feature_card, footer

FEATURES = [
    ("🧠", "EEG Visualization", "Interactive, scrollable multi-channel EEG traces rendered with Plotly."),
    ("📊", "PSD Analysis", "Welch power spectral density per channel with adjustable frequency range."),
    ("🧬", "ICA Artifact Removal", "Fit ICA, inspect components, and exclude eye/muscle artifacts interactively."),
    ("🌈", "Frequency Band Extraction", "Isolate Delta, Theta, Alpha, Beta and Gamma with one click."),
    ("📈", "Feature Extraction", "Per-channel band power tables, heatmaps and radar profiles."),
    ("⬇", "CSV Export", "Download filtered signals, PSD figures and band power tables."),
]


def render():
    hero(
        "EEG Frequency Band Analyzer",
        "A research-grade dashboard for exploring EEG recordings — filter, decompose, "
        "and quantify brain-wave activity across Delta, Theta, Alpha, Beta and Gamma "
        "bands, powered by MNE-Python.",
    )

    _, mid, _ = st.columns([1, 1, 1])
    with mid:
        if st.button("🚀  Get Started", use_container_width=True):
            st.session_state["_nav_override"] = "📂 Upload EEG"
            st.rerun()

    st.write("")
    st.write("")

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(FEATURES):
        with cols[i % 3]:
            feature_card(icon, title, desc)

    st.write("")
    st.markdown(
        """
        <div class="glass-card">
        <b>How it works</b><br><br>
        1. Upload an .fif / .edf / .gdf recording, or load the built-in MNE sample dataset.<br>
        2. Inspect raw EEG quality — sampling rate, channel count, bad channels.<br>
        3. Apply filtering and remove artifacts with ICA.<br>
        4. Extract frequency bands and quantify power per channel.<br>
        5. Export everything as CSV for your report or paper.
        </div>
        """,
        unsafe_allow_html=True,
    )

    footer()
