import mne
import matplotlib.pyplot as plt

sample_path = mne.datasets.sample.data_path()

raw_file = sample_path / "MEG" / "sample" / "sample_audvis_filt-0-40_raw.fif"

raw = mne.io.read_raw_fif(raw_file, preload=True)

raw.pick("eeg")

raw.plot_sensors(
    kind="topomap",
    show_names=True
)

plt.show()