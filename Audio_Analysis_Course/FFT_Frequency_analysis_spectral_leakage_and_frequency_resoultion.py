# FFT frequency analysis: spectral leakage and frequency resolution exercise 

import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

fs = 1000                                 
t = np.arange(0, 1, 1/fs)                 
signal = np.sin(2*np.pi*50*t) + np.sin(2*np.pi*55*t)   

pad = 4096                                 
freq = np.fft.rfftfreq(pad, 1/fs)        

def fft_curve(x, window):
    result = np.abs(np.fft.rfft(x * window, n=pad))
    return result / result.max()           

short = signal[:100]
rect = fft_curve(short, np.ones(100))
hann = fft_curve(short, np.hanning(100))
hamm = fft_curve(short, np.hamming(100))

# 2) short vs long signal, same window
short_fft = fft_curve(signal[:100], np.hanning(100))
long_fft = fft_curve(signal[:1000], np.hanning(1000))

plt.figure(figsize=(12, 9))

plt.subplot(2, 1, 1)
plt.plot(freq, rect, label="Rectangular")
plt.plot(freq, hann, label="Hann")
plt.plot(freq, hamm, label="Hamming")
plt.title("Spectral leakage: effect of window choice")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.xlim(0, 140)
plt.legend()
plt.grid(True)

plt.subplot(2, 2, 3)
plt.plot(freq, short_fft)
plt.axvline(50, color="r", linestyle="--")
plt.axvline(55, color="r", linestyle="--")
plt.title("Short window: N = 100 (0.1 s)\nbin spacing = 10 Hz")
plt.xlabel("Frequency (Hz)")
plt.xlim(35, 70)
plt.grid(True)

plt.subplot(2, 2, 4)
plt.plot(freq, long_fft)
plt.axvline(50, color="r", linestyle="--")
plt.axvline(55, color="r", linestyle="--")
plt.title("Long window: N = 1000 (1 s)\nbin spacing = 1 Hz")
plt.xlabel("Frequency (Hz)")
plt.xlim(35, 70)
plt.grid(True)

plt.tight_layout()
plt.show()