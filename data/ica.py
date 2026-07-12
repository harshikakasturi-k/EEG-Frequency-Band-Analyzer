import mne

sample_path = mne.datasets.sample.data_path()
raw_file = sample_path / "MEG" / "sample" / "sample_audvis_filt-0-40_raw.fif"

raw = mne.io.read_raw_fif(raw_file, preload=True)

raw.pick("eeg")
raw.filter(1, 40)

ica = mne.preprocessing.ICA(
    n_components=20,
    random_state=97,
    max_iter="auto"
)

ica.fit(raw)

ica.exclude = [0, 10, 11, 12, 13, 15, 16, 17, 19]

cleaned = raw.copy()
ica.apply(cleaned)

cleaned.plot(
    duration=10,
    n_channels=20,
    title="EEG after ICA",
    block=True
)