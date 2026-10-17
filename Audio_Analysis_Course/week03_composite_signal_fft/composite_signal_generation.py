import numpy as np
import matplotlib.pyplot as plt

#Sampling parameters

fs = 1000                  # sampling rate [Hz]
T = 2.0                    # duration [s]
N = int(fs * T)            # number of samples = 2000
t = np.arange(N) / fs      # time axis: 0, 0.001, ..., 1.999 s

#Define the sine components: (amplitude, frequency in Hz)
components = [(2.0, 50), (1.0, 120), (0.5, 200)]

#Build each sine and the composite (sum)
sines = [A * np.sin(2 * np.pi * f * t) for A, f in components]
x = np.sum(sines, axis=0)

print(f"Samples: {N}, time step: {1/fs} s")
print("First 5 composite values:", np.round(x[:5], 3))

#Plot components and composite (first 100 ms) ----
fig, ax = plt.subplots(4, 1, figsize=(10, 9), sharex=True)
for i, ((A, f), s) in enumerate(zip(components, sines)):
    ax[i].plot(t, s)
    ax[i].set_ylabel("Amplitude")
    ax[i].set_title(f"Component {i+1}: A = {A}, f = {f} Hz")
ax[3].plot(t, x, color="black")
ax[3].set_title("Composite signal = sum of the three")
ax[3].set_xlabel("Time [s]"); ax[3].set_ylabel("Amplitude")
ax[3].set_xlim(0, 0.1)
plt.tight_layout()
plt.savefig("part1_signal.png", dpi=120)