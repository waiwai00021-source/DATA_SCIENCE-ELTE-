# Question 1 _ Generate a veryy high_resolution sine wave to approximate the continuous signal.
# Question 2 _Sample the signal at each of the three sampling frequencies 
# 44.1 kHz
#8 kHz
#1.5 kHz
# Question 3 _ Demonstrate the Nyquist criterion 
# Question 4 _ Demonstrate the alias frequency 

# Solutions 

import numpy as np
import matplotlib.pyplot as plt

# Signal Parameters
f_sig = 1000.0       # Original continuous signal frequency = 1 kHz (1000 Hz)
A = 1.0              # Peak amplitude
phi = 0.0            # Phase shift
duration = 0.005   # 5 milliseconds

# Continuous Reference (Oversampled at 100 kHz)
fs_cont = 100000.0   # 100 kHz continuous approximation
t_cont = np.linspace(0, duration, int(fs_cont * duration), endpoint=False)
x_cont = A * np.sin(2 * np.pi * f_sig * t_cont + phi)

# Solution 2: Sample at Three Frequencies
fs_list = [44100.0, 8000.0, 1500.0]  # 44.1 kHz, 8 kHz, 1.5 kHz

sampled_signals = []
for fs in fs_list:
    t_s = np.arange(0, duration, 1/fs)
    x_s = A * np.sin(2 * np.pi * f_sig * t_s + phi)
    sampled_signals.append((fs, t_s, x_s))

# Solutions for 3 & 4: Nyquist Criterion & Aliasing

nyquist_limit = f_sig * 2  # Nyquist rate = 2000 Hz (2 kHz)

print(f"--- Signal Analysis ---")
print(f"Signal Frequency (f_sig): {f_sig} Hz")
print(f"Nyquist Rate Requirement (2 * f_sig): {nyquist_limit} Hz\n")

for fs, t_s, x_s in sampled_signals:
    if fs >= nyquist_limit:
        print(f"Sampling Rate: {fs/1000} kHz -> SATISFIES Nyquist Criterion (No Aliasing)")
    else:
        # Calculate alias frequency using closest harmonic fold-over
        k = round(f_sig / fs)
        f_alias = abs(f_sig - k * fs)
        print(f"Sampling Rate: {fs/1000} kHz -> VIOLATES Nyquist Criterion!")
        print(f"  └─> Apparent Alias Frequency (f_alias): {f_alias} Hz\n")

# Plotting Results

fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharex=True)

for idx, (fs, t_s, x_s) in enumerate(sampled_signals):
    ax = axes[idx]
    
    # Plot ground truth continuous wave
    ax.plot(t_cont * 1000, x_cont, color='lightgray', linestyle='--', label='Continuous (1 kHz)')
    
    # Plot discrete sample points
    ax.stem(t_s * 1000, x_s, linefmt='C0-', markerfmt='C0o', basefmt=' ', label=f'Samples (fs = {fs/1000} kHz)')
    
    # If aliased, plot reconstructed lower-frequency alias wave
    if fs < nyquist_limit:
        k = round(f_sig / fs)
        f_alias = abs(f_sig - k * fs)
        x_alias = A * np.sin(2 * np.pi * f_alias * t_cont + phi)
        ax.plot(t_cont * 1000, x_alias, 'r-', linewidth=1.5, label=f'Reconstructed Alias Wave ({f_alias} Hz)')
    
    ax.set_ylabel('Amplitude')
    ax.set_title(f'Sampling Rate: {fs/1000} kHz')
    ax.grid(True)
    ax.legend(loc='upper right')

axes[-1].set_xlabel('Time (ms)')
plt.tight_layout()
plt.show()