import argparse
import librosa
import noisereduce as nr
import soundfile as sf

def denoise_audio(input_file, output_file, noise_reduction=0.5, n_fft=2048, hop_length=512):
    """
    Denoises an audio file by applying noise reduction.
    
    :param input_file: Path to input audio file.
    :param output_file: Path to save cleaned audio file.
    :param noise_reduction: Float, how much noise to reduce (0 to 1, default 0.5).
    """
    # Load audio file
    audio, sr = librosa.load(input_file, sr=None)
    
    # Estimate noise using the first 0.5 seconds (adjust as needed)
    noise_sample = audio[:int(sr * 0.5)]
    
    # Reduce noise
    reduced_noise = nr.reduce_noise(y=audio, sr=sr, y_noise=noise_sample, prop_decrease=noise_reduction)
    
    # Save output file
    sf.write(output_file, reduced_noise, sr)
    print(f"Denoised audio saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Denoise an audio file.")
    parser.add_argument("input", help="Path to input audio file.")
    parser.add_argument("output", help="Path to output denoised audio file.")
    parser.add_argument("--reduction", type=float, default=0.5, help="Noise reduction factor (0 to 1, default 0.5).")

    
    args = parser.parse_args()
    
    denoise_audio(args.input, args.output, args.reduction)
