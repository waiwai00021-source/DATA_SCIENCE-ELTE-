#Question 1  A sound wave has a wavelength of 1.5 m and a frequency of 220 Hz. Calculate the velocity of the wave.
wavelength = 1.5  # meters
frequency = 220  # Hz
velocity = wavelength * frequency
print(f"The velocity of the wave is {velocity} m/s.")
# velocity of the wave is 330.0 m/s.

#Question 2 The time period of a sound wave is 0.004 s. Find the frequency and state whether the sound is audible to humans.
period = 0.004  # seconds
frequency = 1 / period
print(f"The frequency of the wave is {frequency} Hz.")

# Check if the sound is audible to humans (typically 20 Hz to 20,000 Hz)
if 20 <= frequency <= 20000:
    print("The sound is audible to humans.")
else:
    print("The sound is not audible to humans.")

# Question 3 A sound wave travels with a velocity of 340 m/s. How many vibrations will it complete in 5 seconds if its wavelength is 2 m?
velocity = 340  # m/s
wavelength = 2  # meters
frequency = velocity / wavelength  # frequency = velocity / wavelength
time = 5  # seconds
vibrations = frequency * time
print(f"The number of vibrations completed in 5 seconds is {vibrations}.")
# The number of vibrations completed in 5 seconds is 850.0.

# Question 4 A sound wave travels through a medium with a velocity of 360 m/s. If its frequency is increased by 40 Hz, the wavelength decreases by 0.5 m. Find the original frequency of the wave.
import math

velocity = 360  # m/s
frequency_increase = 40  # Hz
wavelength_decrease = 0.5  # m

# Let the original frequency be f.
# v/f - 0.5 = v/(f + 40)

# This gives:
# f^2 + 40f - 28800 = 0

a = 1
b = 40
c = -28800

# Quadratic formula
f1 = (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)
f2 = (-b - math.sqrt(b**2 - 4*a*c)) / (2*a)

print("Possible solutions:", f1, "Hz and", f2, "Hz")

# Frequency cannot be negative
original_frequency = f1

print("The original frequency is", original_frequency, "Hz.")

# The orignal frequency is 150.88 Hz.

#Question 5 Two sound waves travel through the same medium. The frequency of the first wave is twice that of the second wave, while their wavelengths differ by 1.2 m. If the velocity of sound in the medium is 300 m/s, find the frequencies of both waves.

velocity = 300  # m/s
wavelength_difference = 1.2  # m

# Let the frequency of the second wave be f.
# The first frequency is twice the second frequency.

# wavelength_difference = 300/f - 300/(2f)
# wavelength_difference = 150/f

frequency_second = 150 / wavelength_difference
frequency_first = 2 * frequency_second

print("Frequency of the first wave:", frequency_first, "Hz")
print("Frequency of the second wave:", frequency_second, "Hz")

#Question 6 A sound wave A has twice the frequency of sound wave B. If the wavelength of wave A is 1 m less than that of wave B and both travel with the same velocity, find the velocity of the waves.
# Wave A has twice the frequency of wave B
# Wavelength of A is 1 m less than wavelength of B

wavelength_B = 2  # m
wavelength_A = wavelength_B - 1  # m

print("Wavelength of wave A:", wavelength_A, "m")
print("Wavelength of wave B:", wavelength_B, "m")
print("Velocity cannot be calculated numerically without a frequency value.")