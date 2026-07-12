import streamlit as st
from ui.components import no_data_warning, footer, success_toast, error_box
from utils.plotting import eeg_time_series
from utils.backend_bridge import run_filter


def render():
    st.title("🎚 Filtering")
    st.caption("Runs your `data/filter.py` implementation.")

    if not st.session_state.get("raw"):
        no_data_warning("Filtering")
        footer()
        return

    raw = st.session_state["raw"]

    mode = st.radio(
        "Filter type",
        ["High-pass", "Low-pass", "Band-pass"],
        horizontal=True,
    )

    l_freq, h_freq = None, None
    if mode == "High-pass":
        l_freq = st.slider("High-pass cutoff (Hz)", 0.1, 20.0, 1.0, 0.1,
                            help="Removes slow drifts below this frequency.")
    elif mode == "Low-pass":
        h_freq = st.slider("Low-pass cutoff (Hz)", 5.0, 100.0, 40.0, 1.0,
                            help="Removes high-frequency noise above this frequency.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            l_freq = st.slider("Low cutoff (Hz)", 0.1, 20.0, 1.0, 0.1)
        with c2:
            h_freq = st.slider("High cutoff (Hz)", 5.0, 100.0, 40.0, 1.0)

    if st.button("▶️  Apply Filter", use_container_width=False):
        with st.spinner("Filtering signal..."):
            try:
                filtered = run_filter(raw, l_freq, h_freq)
                st.session_state["raw_filtered"] = filtered
                st.session_state["raw_ica_clean"] = None
                st.session_state["l_freq"], st.session_state["h_freq"] = l_freq, h_freq
                success_toast("Filter applied.")
            except Exception as e:
                error_box("Filtering failed.", e)

    st.divider()

    active = st.session_state.get("raw_filtered")
    if active is not None:
        st.markdown("#### Filtered EEG Preview")
        n_channels = st.slider("Channels to display", 1, min(32, len(active.ch_names)), min(8, len(active.ch_names)))
        window = st.slider("Preview window (s)", 1.0, min(30.0, float(active.times[-1])), 5.0)
        try:
            data, times = active.get_data(
                picks=active.ch_names[:n_channels], stop=int(window * active.info["sfreq"]), return_times=True
            )
            fig = eeg_time_series(times, data * 1e6, active.ch_names[:n_channels], title="Filtered EEG")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            error_box("Could not render filtered signal.", e)
    else:
        st.info("Apply a filter above to see the result here.")

    footer()
