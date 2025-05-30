import argparse
import librosa
import numpy as np

def calculate_mse(original, processed):
    return np.mean((original - processed) ** 2)

def calculate_snr(original, processed):
    mse = calculate_mse(original, processed)
    if mse == 0:
        return np.inf
    signal_power = np.sum(original ** 2)
    noise_power = np.sum((original - processed) ** 2)
    snr = 10 * np.log10(signal_power / noise_power)
    return snr



def process_audio(original_path, processed_path):
    # Load the original MP3 file
    orig_signal, sr = librosa.load(original_path, sr=None)
    
    # Load the processed MP3 file with the same sampling rate
    proc_signal, proc_sr = librosa.load(processed_path, sr=sr)
    
    # Ensure both signals are the same length
    min_length = min(len(orig_signal), len(proc_signal))
    orig_signal = orig_signal[:min_length]
    proc_signal = proc_signal[:min_length]
    
    # Compute metrics
    mse_value = calculate_mse(orig_signal, proc_signal)
    snr_value = calculate_snr(orig_signal, proc_signal)
    
    return mse_value, snr_value

def main():
    parser = argparse.ArgumentParser(description="Compute MSE and SNR between original and processed audio files.")
    parser.add_argument("original", help="Path to the original MP3 file")
    parser.add_argument("processed", help="Path to the processed MP3 file")
    
    args = parser.parse_args()
    mse_value, snr_value = process_audio(args.original, args.processed)
    print(f"MSE: {mse_value}")
    print(f"SNR (dB): {snr_value}")

if __name__ == "__main__":
    main()