# Audio Analysis – Practice: 'A' vs 'S' binary classification
# Pipeline: one recording -> split into clips -> bandpass 80 Hz–8 kHz -> gentle spectral gating
#           -> Mel-spectrogram features -> scaler + classifier
import os
import shutil
import numpy as np
import pandas as pd
import librosa
import librosa.display
import soundfile as sf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# ================= CONFIG: change values here only =================
script_dir = os.path.dirname(os.path.abspath(__file__))       # folder of this .py file
input_file = os.path.join(script_dir, "a_s_recording.wav")    # the single recording (converted with afconvert)
output_dir = os.path.join(script_dir, "recordings")           # split clips go to A/ and S/
labels = ["A", "S"]
order = "blocks"        # "blocks" = all A then all S, "alternate" = A, S, A, S...
sr = 22050              # sample rate (Hz)

top_db = 30             # splitting: silence threshold (lower = stricter)
min_len = 0.2           # splitting: ignore sounds shorter than 0.2 s

low_hz = 80             # bandpass lower edge (removes hum / rumble)
high_hz = 8000          # bandpass upper edge (removes very high hiss)
noise_pct = 10          # quietest 10% of frames = noise estimate
gate_factor = 1.5       # bins below 1.5 x noise level are treated as noise
floor = 0.3             # noise bins are reduced to 30%, not muted (gentle gating)

n_mels = 64             # Mel bands
n_mfcc = 13             # MFCC coefficients (only for the comparison table)
test_size = 0.25
seed = 42

# ================= 1. SPLIT THE RECORDING INTO CLIPS =================
shutil.rmtree(output_dir, ignore_errors=True)                       # delete old clips so each run starts fresh
signal, _ = librosa.load(input_file, sr=sr)
intervals = librosa.effects.split(signal, top_db=top_db)             # [start, end] of each sound
intervals = [iv for iv in intervals if (iv[1] - iv[0]) / sr >= min_len]
n = len(intervals)
print("Sounds found:", n)

if order == "blocks":
    clip_labels = ["A"] * (n // 2) + ["S"] * (n - n // 2)
else:
    clip_labels = ["A" if i % 2 == 0 else "S" for i in range(n)]

for label in labels:
    os.makedirs(os.path.join(output_dir, label), exist_ok=True)

for i, (start, end) in enumerate(intervals):
    count = clip_labels[:i + 1].count(clip_labels[i])
    path = os.path.join(output_dir, clip_labels[i], f"{clip_labels[i]}_{count:02d}.wav")
    sf.write(path, signal[start:end], sr)

print(pd.Series(clip_labels).value_counts().rename("clips"))

# ================= 2. NOISE FILTERING + 3. FEATURES =================
freqs = librosa.fft_frequencies(sr=sr)
band = (freqs >= low_hz) & (freqs <= high_hz)                        # True inside 80 Hz–8 kHz

mel_list = []
mfcc_list = []
y_list = []
example = {}                                                         # one raw/clean pair per letter for plotting

for label in labels:
    folder = os.path.join(output_dir, label)
    for file in sorted(os.listdir(folder)):
        raw, _ = librosa.load(os.path.join(folder, file), sr=sr)

        # bandpass filter: zero all frequencies outside 80 Hz–8 kHz
        stft = librosa.stft(raw)
        mag = np.abs(stft)
        stft[~band, :] = 0

        # gentle spectral gating: learn noise from the quietest frames, turn noise bins down to 30%
        frame_energy = mag.sum(axis=0)
        quiet = frame_energy <= np.percentile(frame_energy, noise_pct)
        noise_profile = mag[:, quiet].mean(axis=1, keepdims=True)
        mask = np.where(mag > gate_factor * noise_profile, 1.0, floor)
        clean = librosa.istft(stft * mask, length=len(raw))

        # Mel-spectrogram (dB) -> mean + std over time = one fixed-size vector per clip
        mel_db = librosa.power_to_db(librosa.feature.melspectrogram(y=clean, sr=sr, n_mels=n_mels), ref=np.max)
        mel_list.append(np.concatenate([mel_db.mean(axis=1), mel_db.std(axis=1)]))

        # MFCC from the same clean signal (only used in the comparison table)
        mfcc = librosa.feature.mfcc(y=clean, sr=sr, n_mfcc=n_mfcc)
        mfcc_list.append(np.concatenate([mfcc.mean(axis=1), mfcc.std(axis=1)]))

        y_list.append(labels.index(label))
        example.setdefault(label, (raw, clean))

X_mel = np.array(mel_list)
X_mfcc = np.array(mfcc_list)
y = np.array(y_list)                                                 # A -> 0, S -> 1
print("X_mel shape:", X_mel.shape)

# ================= PLOT: raw vs filtered Mel-spectrogram =================
fig, axes = plt.subplots(2, 2, figsize=(11, 6))
for col, label in enumerate(labels):
    for row, (name, audio) in enumerate(zip(["raw", "filtered"], example[label])):
        mel_db = librosa.power_to_db(librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=n_mels), ref=np.max)
        librosa.display.specshow(mel_db, sr=sr, x_axis="time", y_axis="mel", ax=axes[row, col])
        axes[row, col].set_title(f"'{label}' – {name}")
plt.tight_layout()
plt.savefig(os.path.join(script_dir, "mel_raw_vs_filtered.png"), dpi=120)
plt.close()                                                          # plot saved as png; close so the script continues

# ================= 4. CLASSIFICATION =================
# 5-fold cross-validation: more honest than one small test split with only ~40 clips
feature_sets = {"Mel-spectrogram": X_mel, "MFCC (comparison)": X_mfcc}
models = {"LogReg": LogisticRegression(max_iter=1000), "SVM": SVC(kernel="rbf")}
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)

results = []
for feat_name, X in feature_sets.items():
    for model_name, model in models.items():
        scores = cross_val_score(make_pipeline(StandardScaler(), model), X, y, cv=cv)
        results.append({"features": feat_name, "model": model_name,
                        "cv_accuracy": round(scores.mean(), 3), "cv_std": round(scores.std(), 3)})
print(pd.DataFrame(results).to_string(index=False))

# final model: Mel-spectrogram features + Logistic Regression
X_train, X_test, y_train, y_test = train_test_split(X_mel, y, test_size=test_size, stratify=y, random_state=seed)
final_model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
final_model.fit(X_train, y_train)
y_pred = final_model.predict(X_test)

print("\nTest accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=labels))
cm = confusion_matrix(y_test, y_pred)
print(pd.DataFrame(cm, index=[f"true {l}" for l in labels], columns=[f"pred {l}" for l in labels]))
