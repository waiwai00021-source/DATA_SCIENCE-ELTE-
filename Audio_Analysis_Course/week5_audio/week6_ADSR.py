import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

fs = 44100      
duration = 2     
f0 = 440          

# ADSR settings
attack = 0.1         
decay = 0.2          
sustain_level = 0.6  
release_start = 1.6   
release = 0.4        

# Task 1: time axis + fundamental + two harmonics
n_samples = int(fs * duration)              # 88,200 samples
t = np.arange(n_samples) / fs               # t = n / fs
x = np.sin(2 * np.pi * f0 * t)              # 440 Hz, amplitude 1
x += 0.5 * np.sin(2 * np.pi * 2 * f0 * t)   # 880 Hz, amplitude 0.5
x += 0.25 * np.sin(2 * np.pi * 3 * f0 * t)  # 1320 Hz, amplitude 0.25
x = x / np.max(np.abs(x))                   # normalize max value to 1
# Task 2: ADSR envelope function
def adsr(t, attack, decay, sustain_level, release_start, release):
    # corner points of the envelope (time, level)
    times = [0, attack, attack + decay, release_start, release_start + release]
    levels = [0, 1, sustain_level, sustain_level, 0]
    # straight lines between the corners at every t
    return np.interp(t, times, levels)

env = adsr(t, attack, decay, sustain_level, release_start, release)

# Task 3: modulate, then recover the envelope with Hilbert
y = env * x                         # y(t) = E_ADSR(t) * x(t)
analytic = hilbert(y)               # analytic signal z = y + j*H{y}
hilbert_env = np.abs(analytic)      # envelope = |z|

print("Samples:", n_samples)
print("Max |y|:", round(np.max(np.abs(y)), 3))
print("Max Hilbert envelope:", round(np.max(hilbert_env), 3))
print("Mean gap (Hilbert - ADSR):", round(np.mean(hilbert_env - env), 3))

plt.figure(figsize=(12, 5))
plt.fill_between(t, y, color="tab:blue", alpha=0.6, label="Modulated signal y(t)")
plt.plot(t, hilbert_env, color="tab:orange", linewidth=0.5, alpha=0.5, label="Hilbert envelope")
plt.plot(t, env, "k--", linewidth=2, label="Original ADSR curve")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("ADSR envelope curve and Hilbert envelope")
plt.legend(loc="upper right")
plt.grid(alpha=0.3)
plt.savefig("adsr_hilbert.png", dpi=120, bbox_inches="tight")
plt.show()

# plot 2: zoom into 10 ms of the Sustain stage to see why the Hilbert envelope ripples
zoom = (t >= 1.0) & (t <= 1.01)
plt.figure(figsize=(12, 4))
plt.plot(t[zoom], y[zoom], color="tab:blue", label="Modulated signal y(t)")
plt.plot(t[zoom], hilbert_env[zoom], color="tab:orange", label="Hilbert envelope")
plt.plot(t[zoom], env[zoom], "k--", label="Original ADSR curve")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Zoom: 1.00-1.01 s (Sustain)")
plt.legend(loc="upper right")
plt.grid(alpha=0.3)
plt.savefig("adsr_hilbert_zoom.png", dpi=120, bbox_inches="tight")
plt.show()