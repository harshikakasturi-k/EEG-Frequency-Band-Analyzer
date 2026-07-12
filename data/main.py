import mne
import numpy as np
import matplotlib.pyplot as plt
import mne
import mne

import mne
import mne

# Load sample dataset
sample_path = mne.datasets.sample.data_path()

raw_file = sample_path / "MEG" / "sample" / "sample_audvis_filt-0-40_raw.fif"

raw = mne.io.read_raw_fif(raw_file, preload=True)

# Select EEG channels only
raw.pick("eeg")

# Open interactive EEG viewer
raw.plot(
    duration=10,
    n_channels=20,
    scalings="auto",
    title="EEG Signal Visualizer",
    block=True
)

