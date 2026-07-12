import io
import numpy as np
import pandas as pd
import streamlit as st
from ui.components import footer, no_data_warning
from utils.state import active_raw


def render():
    st.title("⬇ Download Center")

    if not st.session_state.get("raw"):
        no_data_warning("Download")
        footer()
        return

    raw = active_raw()

    st.markdown("#### Available Exports")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Filtered / Active EEG (CSV)**")
        if st.button("Prepare EEG CSV", key="prep_eeg_csv"):
            with st.spinner("Building CSV..."):
                data = raw.get_data().T  # (n_samples, n_channels)
                df = pd.DataFrame(data, columns=raw.ch_names)
                df.insert(0, "time_s", raw.times)
                st.session_state["_eeg_csv"] = df.to_csv(index=False).encode("utf-8")
        if st.session_state.get("_eeg_csv"):
            st.download_button(
                "⬇ Download EEG CSV",
                data=st.session_state["_eeg_csv"],
                file_name="eeg_signal.csv",
                mime="text/csv",
            )

    with col2:
        st.markdown("**Band Power Table (CSV)**")
        df_bp = st.session_state.get("band_power_df")
        if df_bp is not None:
            st.download_button(
                "⬇ Download Band Power CSV",
                data=df_bp.to_csv().encode("utf-8"),
                file_name="band_power.csv",
                mime="text/csv",
            )
        else:
            st.info("Compute band power on the **📋 Band Power** page first.")

    st.divider()

    st.markdown("**PSD Result (CSV)**")
    psd_result = st.session_state.get("_psd_result")
    if psd_result:
        freqs, psd_matrix, ch_names = psd_result
        df_psd = pd.DataFrame(psd_matrix.T, columns=ch_names)
        df_psd.insert(0, "frequency_hz", freqs)
        st.download_button(
            "⬇ Download PSD CSV",
            data=df_psd.to_csv(index=False).encode("utf-8"),
            file_name="psd_result.csv",
            mime="text/csv",
        )
    else:
        st.info("Compute a PSD on the **📊 PSD Analysis** page first.")

    footer()
