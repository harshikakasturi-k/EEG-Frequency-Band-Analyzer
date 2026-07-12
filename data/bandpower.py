import mne
import numpy as np
import pandas as pd

# -----------------------------
# Load Dataset
# -----------------------------
sample_path = mne.datasets.sample.data_path()

raw_file = sample_path / "MEG" / "sample" / "sample_audvis_filt-0-40_raw.fif"

raw = mne.io.read_raw_fif(raw_file, preload=True)

# Keep EEG only
raw.pick("eeg")

# Filter
raw.filter(1,40)

# -----------------------------
# Compute PSD
# -----------------------------
psd = raw.compute_psd(
    fmin=0.5,
    fmax=45
)

# PSD values
psds = psd.get_data()

# Frequencies
freqs = psd.freqs

print(psds.shape)
bands = {
    "Delta": (0.5,4),
    "Theta": (4,8),
    "Alpha": (8,13),
    "Beta": (13,30),
    "Gamma": (30,45)
}

features = {}

for band,(low,high) in bands.items():

    idx = np.logical_and(
        freqs >= low,
        freqs <= high
    )

    band_power = psds[:,idx].mean(axis=1)

    features[band] = band_power
    df = pd.DataFrame(features)

# Remove bad channels
raw.drop_channels(raw.info["bads"])

print("Remaining channels:", len(raw.ch_names))
raw.filter(1, 40)

psd = raw.compute_psd(
    fmin=0.5,
    fmax=45
)

psds = psd.get_data()
freqs = psd.freqs


df.insert(
    0,
    "Channel",
    raw.ch_names
)
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("output/eeg_features.csv")

df.plot(
    x="Channel",
    y=["Delta","Theta","Alpha","Beta","Gamma"],
    kind="bar",
    figsize=(16,6)
)

plt.xticks(rotation=90)

plt.tight_layout()

plt.show()
