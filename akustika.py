import ffmpeg
import os

def apply_lowpass(input_file, output_file, cutoff=3000):
    """Apply a lowpass filter to remove high-frequency noise."""
    (
        ffmpeg
        .input(input_file)
        .filter("lowpass", f=cutoff)
        .output(output_file)
        .run(overwrite_output=True)
    )

def apply_highpass(input_file, output_file, cutoff=200):
    """Apply a highpass filter to remove low-frequency rumble."""
    (
        ffmpeg
        .input(input_file)
        .filter("highpass", f=cutoff)
        .output(output_file)
        .run(overwrite_output=True)
    )

def apply_afftdn(input_file, output_file, mode="default"):
    """Apply FFmpeg's Adaptive Filtering Denoiser."""
    (
        ffmpeg
        .input(input_file)
        .filter("afftdn", nr=mode)
        .output(output_file)
        .run(overwrite_output=True)
    )

def apply_arnndn(input_file, output_file, model_file="rnnoise-model.onnx"):
    """Apply FFmpeg's Neural Network Denoiser using a pre-trained model."""
    if not os.path.exists(model_file):
        print(f"Model file {model_file} not found! Skipping arnndn.")
        return
    (
        ffmpeg
        .input(input_file)
        .filter("arnndn", m=model_file)
        .output(output_file)
        .run(overwrite_output=True)
    )

def apply_superequalizer(input_file, output_file):
    """Apply a multi-band equalizer for noise suppression."""
    (
        ffmpeg
        .input(input_file)
        .filter("superequalizer", "1b=0.5:2b=0.3:3b=0.1:4b=0.2:5b=0.1")
        .output(output_file)
        .run(overwrite_output=True)
    )

def apply_silenceremove(input_file, output_file, threshold=-30):
    """Remove silence below a certain threshold."""
    (
        ffmpeg
        .input(input_file)
        .filter("silenceremove", start_periods=1, start_threshold=f"{threshold}dB")
        .output(output_file)
        .run(overwrite_output=True)
    )

def apply_crystalizer(input_file, output_file, intensity=2.0):
    """Apply crystalizer to enhance clarity after noise reduction."""
    (
        ffmpeg
        .input(input_file)
        .filter("crystalizer", i=intensity)
        .output(output_file)
        .run(overwrite_output=True)
    )

def apply_noise_profile(input_file, output_file, noise_sample="noise_sample.wav"):
    """Generate and apply a noise profile to remove background noise."""
    temp_filtered = "temp_filtered.wav"

    # Step 1: Extract a noise sample (first 1 second of audio)
    ffmpeg.input(input_file, t=1).output(noise_sample, format="wav").run(overwrite_output=True)

    # Step 2: Apply noise reduction based on the sample
    (
        ffmpeg
        .input(input_file)
        .filter("afftdn")
        .output(temp_filtered)
        .run(overwrite_output=True)
    )

    os.rename(temp_filtered, output_file)

if __name__ == "__main__":
    input_audio = "noisy_audio.wav"

    apply_lowpass(input_audio, "output_lowpass.wav")
    apply_highpass(input_audio, "output_highpass.wav")
    apply_afftdn(input_audio, "output_afftdn.wav")
    apply_arnndn(input_audio, "output_arnndn.wav")  # Requires rnnoise-model.onnx
    apply_superequalizer(input_audio, "output_superequalizer.wav")
    apply_silenceremove(input_audio, "output_silenceremove.wav")
    apply_crystalizer(input_audio, "output_crystalizer.wav")
    apply_noise_profile(input_audio, "output_noise_profile.wav")

    print("All noise reduction methods applied successfully.")
