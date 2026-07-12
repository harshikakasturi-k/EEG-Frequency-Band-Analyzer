import streamlit as st
from ui.components import no_data_warning, footer, success_toast, error_box
from utils.plotting import band_power_bar, band_power_heatmap, band_power_radar
from utils.backend_bridge import run_band_power, DEFAULT_BANDS
from utils.state import active_raw


def render():
    st.title("📋 Band Power")
    st.caption("Runs your `data/bandpower.py` implementation.")

    if not st.session_state.get("raw"):
        no_data_warning("Band Power")
        footer()
        return

    raw = active_raw()

    if st.button("⚡  Compute Band Power", use_container_width=False):
        with st.spinner("Computing band power across all channels..."):
            try:
                df = run_band_power(raw, DEFAULT_BANDS)
                st.session_state["band_power_df"] = df
                success_toast("Band power computed.")
            except Exception as e:
                error_box("Band power computation failed.", e)

    df = st.session_state.get("band_power_df")
    if df is None:
        st.info("Click **Compute Band Power** to generate tables and charts.")
        footer()
        return

    tab1, tab2, tab3, tab4 = st.tabs(["📋 Table", "📊 Bar Chart", "🔥 Heatmap", "🕸 Radar Chart"])

    with tab1:
        st.dataframe(df.style.format("{:.4f}"), use_container_width=True)
        csv = df.to_csv().encode("utf-8")
        st.download_button(
            "⬇ Download Band Power CSV",
            data=csv,
            file_name="band_power.csv",
            mime="text/csv",
        )

    with tab2:
        st.plotly_chart(band_power_bar(df), use_container_width=True)

    with tab3:
        st.plotly_chart(band_power_heatmap(df), use_container_width=True)

    with tab4:
        st.plotly_chart(band_power_radar(df), use_container_width=True)

    footer()
