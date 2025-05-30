# AkustikaDenoisingProjekt

## Overview

**AkustikaDenoisingProjekt** is a tool for automatically finding the best denoise settings for your audio files.  
It works by generating multiple denoised versions of a noisy audio file (with different noise reduction strengths), then comparing each version to the original clean file using objective metrics (MSE and SNR) to determine which settings yield the best results.

---

## Main Functionality

- **Batch Denoising:**  
  Automatically creates several denoised versions of your noisy audio file, each with a different noise reduction setting.

- **Automated Comparison:**  
  Compares each denoised file to the original clean audio using Mean Squared Error (MSE) and Signal-to-Noise Ratio (SNR) to find the best-performing settings.

- **Visualization:**  
  Plots SNR and MSE against noise reduction settings, highlighting the best result.

---

## How to Use

### 1. Prepare Your Files

- Place your **original clean audio file** (e.g., `OriginalAudio.mp3`) and your **noisy audio file** (e.g., `NoisyAudio.mp3`) in the project directory.

### 2. Generate Denoised Versions

Run the following command to create multiple denoised versions of your noisy file:

```sh
python denoise_multiple_versions.py NoisyAudio.mp3 --output denoised --var 100
```

- `noisy.mp3`: Path to your noisy audio file.
- `--output`: Prefix for the output denoised files (optional).
- `--var`: Number of denoised versions to generate (each with a different setting).

### 3. Compare Denoised Files to Original

Run the comparison script to evaluate all denoised files against your original:

```sh
python Compare_Audio_Batch.py OriginalAudio.mp3
```

- This will calculate MSE and SNR for each denoised file and display a plot showing which settings performed best.

---

### Example with Provided Files

If you have the example files `Erika_Noise.mp3` (noisy) and `Erika_Orig.mp3` (original), use:

```sh
python denoise_multiple_versions.py Erika_Noise.mp3 --output denoised --var 100
python Compare_Audio_Batch.py Erika_Orig.mp3
```

---

## Main Scripts & Functions

### Scripts Used by the User

- **`denoise_multiple_versions.py`**  
  Automates the creation of multiple denoised files with varying settings.  
  Calls `denoise_audio` from [`denoiser.py`](denoiser.py).

- **`Compare_Audio_Batch.py`**  
  Compares all denoised files to the original and visualizes the results.  
  Calls `process_audio` from [`Audio_diff.py`](Audio_diff.py).

---

### Core Functions (Not Always Used Directly by the User)

- **`denoise_audio(input_file, output_file, noise_reduction=0.5, n_fft=2048, hop_length=512)`**  
  (In [`denoiser.py`](denoiser.py))  
  Denoises an audio file using a specified noise reduction level.

- **`process_audio(original_path, processed_path)`**  
  (In [`Audio_diff.py`](Audio_diff.py))  
  Loads two audio files, aligns them, and computes MSE and SNR.

- **`calculate_mse(original, processed)`**  
  (In [`Audio_diff.py`](Audio_diff.py))  
  Calculates Mean Squared Error between two audio signals.

- **`calculate_snr(original, processed)`**  
  (In [`Audio_diff.py`](Audio_diff.py))  
  Calculates Signal-to-Noise Ratio between two audio signals.

- **Advanced FFmpeg-based functions**  
  (In [`akustika.py`](akustika.py))  
  For advanced users:  
  - `apply_lowpass`, `apply_highpass`, `apply_afftdn`, `apply_arnndn`, `apply_superequalizer`, `apply_silenceremove`, `apply_crystalizer`, `apply_noise_profile`  
  These functions apply various audio filters and denoising methods using FFmpeg.

---

## Requirements

- Python 3.x
- [librosa](https://librosa.org/)
- [noisereduce](https://github.com/timsainb/noisereduce)
- [soundfile](https://pysoundfile.readthedocs.io/)
- [matplotlib](https://matplotlib.org/)
- [numpy](https://numpy.org/)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) (for advanced filtering)
- FFmpeg (must be installed and in your PATH)

Install dependencies with:

```sh
pip install librosa noisereduce soundfile matplotlib numpy ffmpeg-python
```

---

## FAQ

### Q: Is it appropriate to use the Erika song (the German lullaby version) as a sample audio file in this project?

**A (by GitHub Copilot):**  
No, it is not inappropriate to use the Erika lullaby version (the German song) as a sample audio file for technical or educational purposes, such as demonstrating audio denoising. However, be mindful of copyright status and avoid distributing copyrighted material without permission. If the file is in the public domain or you have the rights to use it, it is acceptable for your project.

---

## FYI (In Case You're Wondering!)

**Programmer's question:**  
"Is it appropriate to use the Erika song (the German lullaby version) as a sample audio file in this project?"

**GitHub Copilot's response:**  
No, it is not inappropriate to use the Erika lullaby version (the German song) as a sample audio file for technical or educational purposes, such as demonstrating audio denoising. However, be mindful of copyright status and avoid distributing copyrighted material without permission. If the file is in the public domain or you have the rights to use it, it is acceptable for your project.

---

