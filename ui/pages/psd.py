import streamlit as st
from ui.components import no_data_warning, footer, error_box
from ui.theme import PALETTE
from utils.plotting import psd_line_chart
from utils.backend_bridge import run_psd
from utils.state import active_raw


def render():
    st.title("📊 PSD Analysis")
    st.caption("Runs your `data/psd.py` implementation.")

    if not st.session_state.get("raw"):
        no_data_warning("PSD Analysis")
        footer()
        return

    raw = active_raw()

    c1, c2 = st.columns(2)
    with c1:
        fmin, fmax = st.slider("Frequency range (Hz)", 0.0, 100.0, (0.5, 45.0))
    with c2:
        selected = st.multiselect(
            "Channels (leave empty = all)",
            options=raw.ch_names,
            default=raw.ch_names[: min(6, len(raw.ch_names))],
        )

    picks = selected if selected else None

    if st.button("📈  Compute PSD", use_container_width=False):
        with st.spinner("Computing power spectral density..."):
            try:
                freqs, psd_matrix, ch_names = run_psd(raw, fmin, fmax, picks)
                st.session_state["_psd_result"] = (freqs, psd_matrix, ch_names)
            except Exception as e:
                error_box("PSD computation failed.", e)

    result = st.session_state.get("_psd_result")
    if result:
        freqs, psd_matrix, ch_names = result
        fig = psd_line_chart(freqs, psd_matrix, ch_names)
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("ℹ️ Interpreting this chart"):
            st.write(
                "Power is shown in decibels (10·log10 scale), the standard convention for "
                "EEG spectral plots. Peaks in the 8–13 Hz range typically indicate strong "
                "alpha activity, often prominent with eyes closed."
            )
    else:
        st.info("Set your parameters and click **Compute PSD**.")

    footer()
