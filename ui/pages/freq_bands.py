import numpy as np
import streamlit as st
from ui.components import no_data_warning, band_badge, footer, error_box
from ui.theme import BAND_COLORS, BAND_RANGES, BAND_DESCRIPTIONS
from utils.plotting import band_waveform
from utils.state import active_raw

BANDS = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]


def render():
    st.title("🌈 Frequency Bands")
    st.caption("Filters the active EEG into a specific brain-wave band and shows the result.")

    if not st.session_state.get("raw"):
        no_data_warning("Frequency Bands")
        footer()
        return

    raw = active_raw()

    cols = st.columns(5)
    clicked_band = None
    for i, band in enumerate(BANDS):
        with cols[i]:
            lo, hi = BAND_RANGES[band]
            st.markdown(
                f"""
                <div style="text-align:center;margin-bottom:6px;">
                {band_badge_html(band)}
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"{band}\n{lo}-{hi} Hz", key=f"band_btn_{band}", use_container_width=True):
                clicked_band = band

    if clicked_band:
        st.session_state["_active_band"] = clicked_band

    active_band = st.session_state.get("_active_band")

    if active_band:
        lo, hi = BAND_RANGES[active_band]
        st.divider()
        c1, c2 = st.columns([2, 1])
        with c2:
            st.markdown(f"### {active_band}")
            st.markdown(f"**Range:** {lo}–{hi} Hz")
            st.markdown(f"**Brain state:** {BAND_DESCRIPTIONS[active_band]}")
            channel = st.selectbox("Channel to preview", raw.ch_names, key="band_channel_select")
            window = st.slider("Window (s)", 1.0, min(30.0, float(raw.times[-1])), 8.0, key="band_window")

        with c1:
            with st.spinner(f"Filtering into {active_band} band ({lo}-{hi} Hz)..."):
                try:
                    band_raw = raw.copy().pick([channel])
                    band_raw.filter(l_freq=lo, h_freq=hi, verbose=False)
                    sfreq = band_raw.info["sfreq"]
                    stop_idx = int(window * sfreq)
                    data, times = band_raw.get_data(stop=stop_idx, return_times=True)
                    signal = data[0] * 1e6
                    fig = band_waveform(times, signal, active_band, title=f"{active_band} Band — {channel}")
                    st.plotly_chart(fig, use_container_width=True)
                    st.session_state.setdefault("band_waveforms", {})[active_band] = (times, signal)
                except Exception as e:
                    error_box("Could not compute this band's waveform.", e)
    else:
        st.info("Click a band above to filter and preview the EEG signal for that frequency range.")

    footer()


def band_badge_html(band):
    color = BAND_COLORS[band]
    return f'<span class="band-badge" style="background:{color};">{band}</span>'
