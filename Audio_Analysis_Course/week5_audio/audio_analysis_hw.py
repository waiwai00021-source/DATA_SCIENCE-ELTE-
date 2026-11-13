import os
import parselmouth
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---- change these ----
folder = os.path.dirname(os.path.abspath(__file__))   # the folder this script is in
file_1 = os.path.join(folder, "Audio_File1.wav")      # first audio file
file_2 = os.path.join(folder, "Audio_File2.wav")      # second audio file
name_1 = "Member 1"                                   # label for plots and tables
name_2 = "Member 2"
# ----------------------

snd_1 = parselmouth.Sound(file_1)   # load file 1
snd_2 = parselmouth.Sound(file_2)   # load file 2

info = pd.DataFrame({
    "speaker": [name_1, name_2],
    "duration_s": [snd_1.get_total_duration(), snd_2.get_total_duration()],
    "sample_rate_Hz": [snd_1.sampling_frequency, snd_2.sampling_frequency],
    "channels": [snd_1.n_channels, snd_2.n_channels],
})
print(info)

# ---- Cell 2: waveforms ----
fig, ax = plt.subplots(2, 1, figsize=(10, 5), sharex=True)

ax[0].plot(snd_1.xs(), snd_1.values[0], linewidth=0.5)   # time vs amplitude
ax[0].set_title(f"Waveform – {name_1}")
ax[0].set_ylabel("Amplitude")

ax[1].plot(snd_2.xs(), snd_2.values[0], linewidth=0.5, color="tab:orange")
ax[1].set_title(f"Waveform – {name_2}")
ax[1].set_ylabel("Amplitude")
ax[1].set_xlabel("Time (s)")

plt.tight_layout()
plt.savefig(os.path.join(folder, "waveforms.png"), dpi=150)   # save for your report
plt.show()