# Audio Analysis Course

Weekly Python exercises from the Audio Analysis course at ELTE. Each week has its own folder with the code, a short README, and the figures it produces.

## Weekly projects

| Week | Topic | What it shows | Folder |
|:---:|---|---|---|
| 1 | Wave basics | Frequency, period and wavelength of a sound wave | [week01_wave_basics](week01_wave_basics) |
| 2 | Sampling and aliasing | Nyquist criterion and what happens when it is broken | [week02_sampling_nyquist_aliasing](week02_sampling_nyquist_aliasing) |
| 3 | Composite signals and FFT | Build a signal from sine waves and recover them with the FFT | [week03_composite_signal_fft](week03_composite_signal_fft) |
| 4 | Spectral leakage and resolution | Window choice, signal length and zero-padding | [week04_fft_spectral_leakage_resolution](week04_fft_spectral_leakage_resolution) |

## Setup

```bash
pip install numpy matplotlib
```

Then open a week folder and run its script, for example:

```bash
cd week04_fft_spectral_leakage_resolution
python fft_spectral_leakage_resolution.py
```

## Structure

```
Audio_Analysis_Course/
├── README.md
├── week01_wave_basics/
│   ├── README.md
│   ├── wave_calculator.py
│   └── homework_wave_problems.py
├── week02_sampling_nyquist_aliasing/
├── week03_composite_signal_fft/
└── week04_fft_spectral_leakage_resolution/
```

Each week folder also has a `figures/` folder with the plots its scripts produce.

## Author

Wai Wai Lwin
