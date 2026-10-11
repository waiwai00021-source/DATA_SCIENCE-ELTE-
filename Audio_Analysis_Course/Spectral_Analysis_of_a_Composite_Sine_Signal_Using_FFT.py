import numpy as np
import matplotlib.pyplot as plt

# ---------- Settings you can change ----------
fs = 1000          # sampling frequency (Hz)
duration = 1.0     # signal length (seconds)

f1 = 50            # frequency of component 1 (Hz)
a1 = 1.0           # amplitude of component 1

f2 = 120           # frequency of component 2 (Hz)
a2 = 0.5           # amplitude of component 2

f3 = 200           # frequency of component 3 (Hz)
a3 = 0.3           # amplitude of component 3
# ---------------------------------------------

# Time axis
N = int(fs * duration)             # number of samples
t = np.arange(N) / fs              # time values in seconds

# Generate the sine components
s1 = a1 * np.sin(2 * np.pi * f1 * t)
s2 = a2 * np.sin(2 * np.pi * f2 * t)
s3 = a3 * np.sin(2 * np.pi * f3 * t)

# Composite signal
signal = s1 + s2 + s3

# Spectral analysis with FFT
fft_vals = np.fft.rfft(signal)             # FFT for real signals (positive freqs only)
freqs = np.fft.rfftfreq(N, d=1/fs)         # matching frequency axis

# Convert FFT output to real amplitudes
amps = np.abs(fft_vals) * 2 / N            # scale so peak height = sine amplitude
amps[0] = amps[0] / 2                      # DC term should not be doubled

# Find the peaks (the components)
threshold = 0.05                           # ignore tiny values (noise / leakage)
peak_idx = []
for i in range(1, len(amps) - 1):
    if amps[i] > threshold and amps[i] > amps[i-1] and amps[i] > amps[i+1]:
        peak_idx.append(i)

# Print amplitude of each detected component
print("Detected components:")
for i in peak_idx:
    print(f"Frequency = {freqs[i]:.1f} Hz, Amplitude = {amps[i]:.3f}")

# Plot time domain
plt.figure(figsize=(10, 7))

plt.subplot(2, 1, 1)
plt.plot(t, signal)                        # composite signal
plt.xlim(0, 0.2)                           # zoom in on the first 0.2 s
plt.title("Composite signal (time domain)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)

# Plot frequency domain
plt.subplot(2, 1, 2)
plt.plot(freqs, amps)                      # amplitude spectrum
plt.xlim(0, 300)
plt.title("Amplitude spectrum (FFT)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.tight_layout()
plt.show()