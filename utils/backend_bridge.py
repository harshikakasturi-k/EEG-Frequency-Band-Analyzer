"""
utils/backend_bridge.py
------------------------
This is the ONLY file that talks to your existing backend scripts in /data.
No EEG algorithm is reimplemented here — every function below is a thin
wrapper that calls into your data/*.py modules.

>>> WHY THIS FILE EXISTS <<<
Your real function names/signatures weren't available when this frontend
was generated, so each wrapper:
  1. Tries a short list of likely function names in your module.
  2. Falls back to a minimal, clearly-marked reference implementation
     ONLY so the app runs end-to-end out of the box.
  3. Prints which path was used to Streamlit's console-free `st.caption`
     debug line in Settings, so you always know if your real code ran.

>>> WHAT YOU SHOULD DO <<<
Open each function below, and either:
  (a) rename a function in your data/*.py file to match one of the
      `candidates` listed, OR
  (b) edit the `candidates` list here to match your actual function name.
Once matched, the fallback branch is never used and your original
algorithm runs untouched.

Expected interface per module (adapt to your real signatures):

  data/main.py
      load_raw_data(file_path: str) -> mne.io.Raw
      load_sample_data() -> mne.io.Raw

  data/filter.py
      apply_filter(raw, l_freq: float | None, h_freq: float | None) -> mne.io.Raw

  data/psd.py
      compute_psd(raw, fmin: float, fmax: float, picks=None) -> (freqs: np.ndarray, psd: np.ndarray, ch_names: list[str])

  data/ica.py
      fit_ica(raw, n_components: int = 15, random_state: int = 97) -> ica_object
      get_sources(ica, raw) -> np.ndarray
      apply_exclusion(ica, raw, exclude: list[int]) -> mne.io.Raw (cleaned)

  data/bandpower.py
      compute_band_power(raw, bands: dict[str, tuple[float, float]]) -> pandas.DataFrame
          (rows = channels, columns = band names)

  data/sensor_map.py
      get_channel_positions(raw) -> dict[str, tuple[float, float]]  (2D x,y per channel)
"""

from __future__ import annotations
import importlib
import sys
import os
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))

DEBUG_LOG: list[str] = []


def _log(msg: str):
    DEBUG_LOG.append(msg)


def _try_import(module_name: str):
    try:
        return importlib.import_module(module_name)
    except Exception as e:
        _log(f"Could not import data.{module_name}: {e}")
        return None


def _find_callable(module, candidates: list[str]):
    if module is None:
        return None
    for name in candidates:
        fn = getattr(module, name, None)
        if callable(fn):
            _log(f"Using {module.__name__}.{name}()")
            return fn
    return None


# ---------------------------------------------------------------------------
# main.py — data loading
# ---------------------------------------------------------------------------
_main_mod = _try_import("main")


def load_raw_from_file(file_path: str):
    fn = _find_callable(_main_mod, ["load_raw_data", "load_raw", "read_raw", "load_file"])
    if fn:
        return fn(file_path)

    _log("Falling back to built-in mne.io.read_raw for file loading")
    import mne
    return mne.io.read_raw(file_path, preload=True, verbose=False)


def load_sample_dataset():
    fn = _find_callable(_main_mod, ["load_sample_data", "load_sample", "get_sample_raw"])
    if fn:
        return fn()

    _log("Falling back to built-in MNE sample dataset")
    import mne
    sample_data_folder = mne.datasets.sample.data_path()
    sample_data_raw_file = os.path.join(
        sample_data_folder, "MEG", "sample", "sample_audvis_raw.fif"
    )
    raw = mne.io.read_raw_fif(sample_data_raw_file, preload=True, verbose=False)
    raw.pick(["eeg"])
    return raw


# ---------------------------------------------------------------------------
# filter.py
# ---------------------------------------------------------------------------
_filter_mod = _try_import("filter")


def run_filter(raw, l_freq: float | None, h_freq: float | None):
    fn = _find_callable(
        _filter_mod, ["apply_filter", "bandpass_filter", "filter_raw", "apply_bandpass"]
    )
    if fn:
        return fn(raw, l_freq, h_freq)

    _log("Falling back to built-in raw.filter()")
    filtered = raw.copy()
    filtered.filter(l_freq=l_freq, h_freq=h_freq, verbose=False)
    return filtered


# ---------------------------------------------------------------------------
# psd.py
# ---------------------------------------------------------------------------
_psd_mod = _try_import("psd")


def run_psd(raw, fmin: float = 0.5, fmax: float = 45.0, picks=None):
    """
    Returns (freqs, psd_matrix, ch_names)
    psd_matrix shape: (n_channels, n_freqs)
    """
    fn = _find_callable(_psd_mod, ["compute_psd", "get_psd", "psd_welch", "calculate_psd"])
    if fn:
        result = fn(raw, fmin, fmax, picks)
        if len(result) == 3:
            return result
        freqs, psd = result
        ch_names = raw.ch_names if picks is None else picks
        return freqs, psd, ch_names

    _log("Falling back to built-in mne raw.compute_psd()")
    spectrum = raw.compute_psd(fmin=fmin, fmax=fmax, picks=picks, verbose=False)
    psd, freqs = spectrum.get_data(return_freqs=True)
    ch_names = spectrum.ch_names
    return freqs, psd, ch_names


# ---------------------------------------------------------------------------
# ica.py
# ---------------------------------------------------------------------------
_ica_mod = _try_import("ica")


def run_ica_fit(raw, n_components: int = 15, random_state: int = 97):
    fn = _find_callable(_ica_mod, ["fit_ica", "run_ica", "compute_ica"])
    if fn:
        return fn(raw, n_components, random_state)

    _log("Falling back to built-in mne.preprocessing.ICA")
    import mne
    filt_raw = raw.copy().filter(l_freq=1.0, h_freq=None, verbose=False)
    ica = mne.preprocessing.ICA(
        n_components=n_components, random_state=random_state, max_iter="auto"
    )
    ica.fit(filt_raw, verbose=False)
    return ica


def get_ica_sources(ica, raw):
    fn = _find_callable(_ica_mod, ["get_sources", "get_ica_sources", "extract_sources"])
    if fn:
        return fn(ica, raw)

    _log("Falling back to built-in ica.get_sources()")
    sources = ica.get_sources(raw)
    return sources.get_data()


def apply_ica_exclusion(ica, raw, exclude: list[int]):
    fn = _find_callable(_ica_mod, ["apply_exclusion", "exclude_components", "remove_components"])
    if fn:
        return fn(ica, raw, exclude)

    _log("Falling back to built-in ica.apply()")
    cleaned = raw.copy()
    ica.exclude = exclude
    ica.apply(cleaned, verbose=False)
    return cleaned


# ---------------------------------------------------------------------------
# bandpower.py
# ---------------------------------------------------------------------------
_bandpower_mod = _try_import("bandpower")

DEFAULT_BANDS = {
    "Delta": (0.5, 4),
    "Theta": (4, 8),
    "Alpha": (8, 13),
    "Beta": (13, 30),
    "Gamma": (30, 45),
}


def run_band_power(raw, bands: dict | None = None) -> pd.DataFrame:
    bands = bands or DEFAULT_BANDS
    fn = _find_callable(
        _bandpower_mod, ["compute_band_power", "band_power", "get_band_power", "bandpower"]
    )
    if fn:
        result = fn(raw, bands)
        if isinstance(result, pd.DataFrame):
            return result
        return pd.DataFrame(result)

    _log("Falling back to built-in Welch-PSD band power calculation")
    spectrum = raw.compute_psd(fmin=0.5, fmax=45.0, verbose=False)
    psd, freqs = spectrum.get_data(return_freqs=True)  # (n_channels, n_freqs)
    ch_names = spectrum.ch_names

    rows = {}
    for ch_idx, ch in enumerate(ch_names):
        row = {}
        for band_name, (lo, hi) in bands.items():
            mask = (freqs >= lo) & (freqs <= hi)
            row[band_name] = float(np.trapz(psd[ch_idx, mask], freqs[mask])) if mask.any() else 0.0
        rows[ch] = row
    return pd.DataFrame.from_dict(rows, orient="index")


# ---------------------------------------------------------------------------
# sensor_map.py
# ---------------------------------------------------------------------------
_sensor_map_mod = _try_import("sensor_map")


def run_sensor_positions(raw) -> dict:
    """Returns {channel_name: (x, y)} in 2D layout coordinates."""
    fn = _find_callable(
        _sensor_map_mod, ["get_channel_positions", "get_sensor_positions", "sensor_layout"]
    )
    if fn:
        return fn(raw)

    _log("Falling back to built-in mne 2D layout positions")
    import mne
    try:
        layout = mne.channels.find_layout(raw.info)
        positions = {name: (pos[0], pos[1]) for name, pos in zip(layout.names, layout.pos)}
        # keep only channels present in raw
        return {ch: positions[ch] for ch in raw.ch_names if ch in positions}
    except Exception as e:
        _log(f"2D layout unavailable ({e}); using montage fallback")
        montage = raw.get_montage()
        if montage is None:
            return {}
        pos_3d = montage.get_positions()["ch_pos"]
        return {ch: (xyz[0], xyz[1]) for ch, xyz in pos_3d.items() if ch in raw.ch_names}
