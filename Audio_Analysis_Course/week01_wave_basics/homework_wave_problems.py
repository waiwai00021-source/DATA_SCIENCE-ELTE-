#Question 1  A sound wave has a wavelength of 1.5 m and a frequency of 220 Hz. Calculate the velocity of the wave.
wavelength = 1.5
frequency = 220
velocity = wavelength * frequency
print("Velocity:", velocity, "m/s")
# velocity of the wave is 330.0 m/s.

#Question 2 The time period of a sound wave is 0.004 s. Find the frequency and state whether the sound is audible to humans.
period = 0.004
frequency = 1 / period
print("Frequency:", frequency, "Hz")

if 20 <= frequency <= 20000:
    print("Audible to humans")
else:
    print("Not audible to humans")

# Question 3 A sound wave travels with a velocity of 340 m/s. How many vibrations will it complete in 5 seconds if its wavelength is 2 m?
velocity = 340
wavelength = 2
time = 5

frequency = velocity / wavelength
vibrations = frequency * time

print("Vibrations in", time, "seconds:", vibrations)

# Question 4 A sound wave travels through a medium with a velocity of 360 m/s. If its frequency is increased by 40 Hz, the wavelength decreases by 0.5 m. Find the original frequency of the wave.
import math

v = 360
increase = 40
decrease = 0.5

a, b, c = 1, increase, -(v * increase) / decrease

f = (-b + (b**2 - 4*a*c)**0.5) / (2*a)
print("Original frequency:", round(f, 2), "Hz")
# The orignal frequency is 150.88 Hz.

#Question 5 Two sound waves travel through the same medium. The frequency of the first wave is twice that of the second wave, while their wavelengths differ by 1.2 m. If the velocity of sound in the medium is 300 m/s, find the frequencies of both waves.

velocity = 300
wavelength_diff = 1.2

# v/f2 - v/(2*f2) = wavelength_diff  →  v/(2*f2) = wavelength_diff
frequency_second = velocity / (2 * wavelength_diff)
frequency_first = 2 * frequency_second

print("Wave 1 frequency:", frequency_first, "Hz")
print("Wave 2 frequency:", frequency_second, "Hz")

#Question 6 A sound wave A has twice the frequency of sound wave B. If the wavelength of wave A is 1 m less than that of wave B and both travel with the same velocity, find the velocity of the waves.
wavelength_B = 2
wavelength_A = wavelength_B - 1

print("Wavelength A:", wavelength_A, "m")
print("Wavelength B:", wavelength_B, "m")
print("Need an actual frequency value to find velocity.")