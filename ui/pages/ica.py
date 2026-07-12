import streamlit as st
from ui.components import no_data_warning, footer, success_toast, error_box
from utils.plotting import ica_components_grid, eeg_time_series
from utils.backend_bridge import run_ica_fit, get_ica_sources, apply_ica_exclusion
from utils.state import active_raw


def render():
    st.title("🧠 ICA — Independent Component Analysis")
    st.caption("Runs your `data/ica.py` implementation.")

    if not st.session_state.get("raw"):
        no_data_warning("ICA")
        footer()
        return

    raw = active_raw()

    n_components = st.slider("Number of components", 5, min(30, len(raw.ch_names)), min(15, len(raw.ch_names)))

    if st.button("🧬  Fit ICA", use_container_width=False):
        with st.spinner("Fitting ICA — this can take a moment..."):
            try:
                ica = run_ica_fit(raw, n_components=n_components)
                st.session_state["ica_obj"] = ica
                success_toast("ICA fitted successfully.")
            except Exception as e:
                error_box("ICA fitting failed.", e)

    ica = st.session_state.get("ica_obj")
    if ica is None:
        st.info("Fit ICA above to inspect components.")
        footer()
        return

    st.divider()
    st.markdown("#### Component Sources")
    try:
        sources = get_ica_sources(ica, raw)
        window = st.slider("Preview window (s)", 1.0, min(30.0, float(raw.times[-1])), 8.0)
        n_show = st.slider("Components to display", 1, min(20, sources.shape[0]), min(8, sources.shape[0]))
        sfreq = raw.info["sfreq"]
        stop_idx = int(window * sfreq)
        times = raw.times[:stop_idx]
        fig = ica_components_grid(sources[:, :stop_idx], times, n_show=n_show)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        error_box("Could not display ICA components.", e)
        sources = None

    st.divider()
    st.markdown("#### Exclude Artifact Components")
    n_total = getattr(ica, "n_components_", n_components) or n_components
    exclude = st.multiselect(
        "Select component indices to exclude (e.g. eye-blink / muscle artifacts)",
        options=list(range(int(n_total))),
        default=[],
    )

    if st.button("🧹  Apply Exclusion & Clean EEG", use_container_width=False):
        with st.spinner("Removing selected components..."):
            try:
                cleaned = apply_ica_exclusion(ica, raw, exclude)
                st.session_state["raw_ica_clean"] = cleaned
                success_toast(f"Removed {len(exclude)} component(s). Cleaned EEG is now active downstream.")
            except Exception as e:
                error_box("Could not apply ICA exclusion.", e)

    cleaned = st.session_state.get("raw_ica_clean")
    if cleaned is not None:
        st.markdown("#### Cleaned EEG Preview")
        try:
            n_channels = min(8, len(cleaned.ch_names))
            data, times = cleaned.get_data(picks=cleaned.ch_names[:n_channels], stop=int(8 * cleaned.info["sfreq"]), return_times=True)
            fig2 = eeg_time_series(times, data * 1e6, cleaned.ch_names[:n_channels], title="ICA-Cleaned EEG")
            st.plotly_chart(fig2, use_container_width=True)
        except Exception as e:
            error_box("Could not render cleaned EEG.", e)

    footer()
