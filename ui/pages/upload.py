import os
import tempfile
import streamlit as st

from ui.components import section_label, success_toast, error_box, footer
from utils.backend_bridge import load_raw_from_file, load_sample_dataset


def render():
    st.title("📂 Upload EEG Recording")
    st.caption("Supported formats: `.fif`, `.edf`, `.gdf` — or load the bundled MNE sample dataset.")

    section_label("Upload your file")
    uploaded = st.file_uploader(
        "Drag and drop an EEG file",
        type=["fif", "edf", "gdf"],
        help="Files stay on this machine / session only — nothing is sent anywhere else.",
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        if uploaded is not None:
            if st.button("⚙️  Process Uploaded File", use_container_width=True):
                with st.spinner("Reading EEG file with MNE-Python..."):
                    try:
                        suffix = os.path.splitext(uploaded.name)[1]
                        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                            tmp.write(uploaded.getbuffer())
                            tmp_path = tmp.name

                        raw = load_raw_from_file(tmp_path)
                        st.session_state["raw"] = raw
                        st.session_state["source_filename"] = uploaded.name
                        st.session_state["raw_filtered"] = None
                        st.session_state["raw_ica_clean"] = None
                        success_toast(f"Loaded '{uploaded.name}' successfully.")
                    except Exception as e:
                        error_box("Could not read this EEG file.", e)

    with col2:
        if st.button("🧪  Load MNE Sample Dataset", use_container_width=True):
            with st.spinner("Downloading / loading MNE sample dataset (first run may take a minute)..."):
                try:
                    raw = load_sample_dataset()
                    st.session_state["raw"] = raw
                    st.session_state["source_filename"] = "MNE Sample Dataset"
                    st.session_state["raw_filtered"] = None
                    st.session_state["raw_ica_clean"] = None
                    success_toast("Sample dataset loaded successfully.")
                except Exception as e:
                    error_box("Could not load the MNE sample dataset.", e)

    st.divider()

    if st.session_state.get("raw") is not None:
        raw = st.session_state["raw"]
        st.markdown("#### ✅ Currently loaded")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Source", st.session_state.get("source_filename", "—"))
        c2.metric("Channels", len(raw.ch_names))
        c3.metric("Sampling Rate", f"{raw.info['sfreq']:.1f} Hz")
        c4.metric("Duration", f"{raw.times[-1]:.1f} s")
        st.info("Head to **📈 Raw EEG** to inspect the signal in detail.")
    else:
        st.warning("No EEG data loaded yet.")

    footer()
