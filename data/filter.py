import mne

sample_path = mne.datasets.sample.data_path()

raw_file = sample_path / "MEG" / "sample" / "sample_audvis_filt-0-40_raw.fif"

raw = mne.io.read_raw_fif(raw_file, preload=True)

raw.pick("eeg")

filtered = raw.copy()

filtered.filter(
    l_freq=1,
    h_freq=40
)

filtered.plot(
    duration=10,
    n_channels=20,
    title="Filtered EEG",
    block=True
)