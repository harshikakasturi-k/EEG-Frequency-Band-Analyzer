import streamlit as st
from ui.components import no_data_warning, stat_pill, footer, error_box
from utils.plotting import eeg_time_series


def render():
    st.title("📈 Raw EEG Signal")

    if not st.session_state.get("raw"):
        no_data_warning("Raw EEG")
        footer()
        return

    raw = st.session_state["raw"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        stat_pill(f"{raw.info['sfreq']:.1f} Hz", "Sampling Frequency")
    with c2:
        stat_pill(str(len(raw.ch_names)), "Channels")
    with c3:
        stat_pill(f"{raw.times[-1]:.1f} s", "Duration")
    with c4:
        n_bad = len(raw.info.get("bads", []))
        stat_pill(str(n_bad), "Bad Channels")

    if raw.info.get("bads"):
        with st.expander("🚩 Bad channel details"):
            st.write(", ".join(raw.info["bads"]))

    st.write("")
    st.markdown("#### Signal Preview")

    max_t = float(raw.times[-1])
    window = st.slider(
        "Time window (seconds)",
        min_value=1.0,
        max_value=min(60.0, max_t) if max_t > 1 else 1.0,
        value=min(10.0, max_t) if max_t > 1 else max_t,
    )
    start = st.slider("Start time (s)", 0.0, max(0.0, max_t - window), 0.0)
    n_channels = st.slider("Channels to display", 1, min(32, len(raw.ch_names)), min(10, len(raw.ch_names)))

    try:
        with st.spinner("Rendering EEG trace..."):
            sfreq = raw.info["sfreq"]
            start_idx = int(start * sfreq)
            stop_idx = int((start + window) * sfreq)
            data, times = raw.get_data(
                picks=raw.ch_names[:n_channels],
                start=start_idx,
                stop=stop_idx,
                return_times=True,
            )
            data_uv = data * 1e6  # volts -> microvolts for readability
            fig = eeg_time_series(times, data_uv, raw.ch_names[:n_channels], title="Raw EEG Trace")
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        error_box("Could not render the EEG trace.", e)

    with st.expander("ℹ️ About this view"):
        st.write(
            "Each trace is vertically offset for readability, same convention used by "
            "clinical EEG viewers. Amplitude is shown in microvolts (µV)."
        )

    footer()
