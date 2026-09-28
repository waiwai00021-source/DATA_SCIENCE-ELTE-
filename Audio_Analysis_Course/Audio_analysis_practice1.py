import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
import soundfile as sf


sound_speed = 343  # meters per second

print("Enter values you know. Leave blank if unknown.")
freq_input = input("Frequency (Hz): ")
period_input = input("Period (s): ")
wavelength_input = input("Wavelength (m): ")

# ---- convert inputs, empty string becomes None ----
frequency = float(freq_input) if freq_input else None
period = float(period_input) if period_input else None
wavelength = float(wavelength_input) if wavelength_input else None

# ---- calculate missing values ----
if frequency is not None and period is None:
    period = 1 / frequency

if frequency is not None and wavelength is None:
    wavelength = sound_speed / frequency

if period is not None and frequency is None:
    frequency = 1 / period

if wavelength is not None and frequency is None:
    frequency = sound_speed / wavelength
    period = 1 / frequency

# ---- print results ----
print(f"[Result] Frequency: {frequency:.5f} Hz")
print(f"[Result] Period: {period:.5f} seconds")
print(rf"[Result] Wavelength ($\lambda$): {wavelength:.5f} meters")

# ---- plot part of the wave ----
time = np.linspace(0, 3 * period, 1000)  # show 3 full cycles
wave = np.sin(2 * np.pi * frequency * time)

plt.plot(time, wave)
plt.title(f"Wave at {frequency:.1f} Hz")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()