# 🧠 EEG Frequency Band Analyzer

A modern, dark-themed EEG signal processing dashboard built with **Streamlit**, **MNE-Python**, and **Plotly**. Upload a recording (or use the MNE sample dataset), filter it, run ICA artifact removal, extract frequency bands, and export quantified band-power features.

## Project Structure

```
EEG_Frequency_Band_Analyzer/
│
├── app.py                     # Streamlit entry point + sidebar navigation
├── data/                      # <-- YOUR EXISTING BACKEND SCRIPTS GO HERE
│   ├── main.py
│   ├── filter.py
│   ├── bandpower.py
│   ├── ica.py
│   ├── psd.py
│   └── sensor_map.py
├── ui/
│   ├── theme.py                # Global CSS (dark glassmorphism theme, colors, band metadata)
│   ├── components.py            # Reusable UI widgets (cards, hero, badges, footer)
│   └── pages/                   # One module per sidebar page
│       ├── home.py
│       ├── upload.py
│       ├── raw_eeg.py
│       ├── filtering.py
│       ├── psd.py
│       ├── ica.py
│       ├── freq_bands.py
│       ├── band_power.py
│       ├── sensor_map.py
│       ├── download.py
│       └── settings.py
├── utils/
│   ├── backend_bridge.py        # THE ONLY FILE THAT CALLS YOUR data/*.py SCRIPTS
│   ├── plotting.py               # Plotly chart builders (themed)
│   └── state.py                  # st.session_state key management
├── output/
├── requirements.txt
└── README.md
```

## Running the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ⚠️ Important: wiring in your real backend

Your original files (`data/filter.py`, `data/psd.py`, `data/ica.py`,
`data/bandpower.py`, `data/sensor_map.py`, `data/main.py`) were **not
included** when this frontend was generated — only their filenames were
known. So that the app is fully runnable immediately, `utils/backend_bridge.py`
was written with:

1. **A documented expected interface** for each module (function names + signatures), and
2. **A safe built-in fallback** (using MNE directly) that only runs if your real function isn't found — so the UI works today even before you drop your files in.

### To connect your real scripts:

1. Copy your actual `main.py`, `filter.py`, `bandpower.py`, `ica.py`, `psd.py`, `sensor_map.py` into the `data/` folder (overwriting the empty placeholders).
2. Open `utils/backend_bridge.py`. Each function has a `candidates` list of likely function names it will try to call on your module, e.g.:

   ```python
   fn = _find_callable(_filter_mod, ["apply_filter", "bandpass_filter", "filter_raw", "apply_bandpass"])
   ```

3. Either rename your function to match one of these candidates, **or** add your actual function name to the list. Once matched, your original algorithm runs — the fallback branch is skipped entirely.
4. Go to the **⚙ Settings** page in the running app — it prints a live log of which function (yours or the fallback) was used for every backend call, so you can confirm the wiring worked.

Expected interface reference:

| File | Expected function | Signature |
|---|---|---|
| `main.py` | `load_raw_data` | `(file_path: str) -> mne.io.Raw` |
| `main.py` | `load_sample_data` | `() -> mne.io.Raw` |
| `filter.py` | `apply_filter` | `(raw, l_freq, h_freq) -> mne.io.Raw` |
| `psd.py` | `compute_psd` | `(raw, fmin, fmax, picks=None) -> (freqs, psd, ch_names)` |
| `ica.py` | `fit_ica` | `(raw, n_components, random_state) -> ica_object` |
| `ica.py` | `get_sources` | `(ica, raw) -> np.ndarray` |
| `ica.py` | `apply_exclusion` | `(ica, raw, exclude: list[int]) -> mne.io.Raw` |
| `bandpower.py` | `compute_band_power` | `(raw, bands: dict) -> pandas.DataFrame` (rows=channels, cols=bands) |
| `sensor_map.py` | `get_channel_positions` | `(raw) -> dict[str, (x, y)]` |

No processing logic was rewritten anywhere in the frontend — every chart is built from data returned by these functions (or the MNE fallback), never from a reimplementation of your algorithms.

## Pages

- **🏠 Home** — product landing page
- **📂 Upload EEG** — `.fif` / `.edf` / `.gdf` upload or MNE sample dataset
- **📈 Raw EEG** — sampling rate, channel count, duration, bad channels, interactive trace
- **🎚 Filtering** — high-pass / low-pass / band-pass, calls `filter.py`
- **📊 PSD Analysis** — channel + frequency range selection, calls `psd.py`
- **🧠 ICA** — fit, inspect components, exclude artifacts, calls `ica.py`
- **🌈 Frequency Bands** — one-click Delta/Theta/Alpha/Beta/Gamma extraction with brain-state explanations
- **📋 Band Power** — table, bar chart, heatmap, radar chart, calls `bandpower.py`, CSV export
- **🗺 Sensor Map** — electrode layout, calls `sensor_map.py`
- **⬇ Download** — CSV export for EEG signal, PSD, band power
- **⚙ Settings** — session reset + backend integration debug log

## Tech stack

Streamlit · MNE-Python · Plotly · Pandas · NumPy — no React/Flask/Django.
