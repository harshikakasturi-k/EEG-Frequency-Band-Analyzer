import streamlit as st
from ui.components import no_data_warning, footer, error_box
from utils.plotting import sensor_map_scatter
from utils.backend_bridge import run_sensor_positions
from utils.state import active_raw


def render():
    st.title("🗺 Sensor Map")
    st.caption("Runs your `data/sensor_map.py` implementation.")

    if not st.session_state.get("raw"):
        no_data_warning("Sensor Map")
        footer()
        return

    raw = active_raw()

    with st.spinner("Computing electrode layout..."):
        try:
            positions = run_sensor_positions(raw)
        except Exception as e:
            error_box("Could not compute sensor positions.", e)
            positions = {}

    if positions:
        fig = sensor_map_scatter(positions)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(
            "No channel position / montage information was found in this recording. "
            "Assign a montage (e.g. `raw.set_montage('standard_1020')`) in your "
            "`data/sensor_map.py` to enable this view."
        )

    footer()
