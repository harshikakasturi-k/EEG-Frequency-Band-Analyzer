import mne
import matplotlib.pyplot as plt

sample_path = mne.datasets.sample.data_path()

raw_file = sample_path / "MEG" / "sample" / "sample_audvis_filt-0-40_raw.fif"

raw = mne.io.read_raw_fif(raw_file, preload=True)

raw.pick("eeg")

psd = raw.compute_psd(
    fmin=1,
    fmax=40
)

psd.plot()

plt.show()