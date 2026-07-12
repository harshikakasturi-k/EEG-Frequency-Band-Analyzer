"""
utils/state.py
---------------
Centralizes st.session_state keys so pages don't rely on magic strings
scattered across the codebase.
"""

import streamlit as st

DEFAULTS = {
    "raw": None,             # mne.io.Raw — originally loaded
    "raw_filtered": None,    # mne.io.Raw — after Filtering page
    "raw_ica_clean": None,   # mne.io.Raw — after ICA exclusion
    "ica_obj": None,         # fitted ICA object
    "band_power_df": None,   # pandas.DataFrame from Band Power page
    "band_waveforms": {},    # {band_name: (times, signal_avg)}
    "source_filename": None,
    "l_freq": 1.0,
    "h_freq": 40.0,
}


def init_state():
    for key, val in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = val


def has_raw() -> bool:
    return st.session_state.get("raw") is not None


def active_raw():
    """Returns the most 'downstream' available raw: ICA-cleaned > filtered > original."""
    return (
        st.session_state.get("raw_ica_clean")
        or st.session_state.get("raw_filtered")
        or st.session_state.get("raw")
    )


def reset_all():
    for key, val in DEFAULTS.items():
        st.session_state[key] = val
