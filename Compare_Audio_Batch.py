import argparse
import glob
import os
import re
import matplotlib.pyplot as plt
from Audio_diff import process_audio  # This must return (mse, snr)

def extract_nr_value(filename):
    """Extract numeric value from filename like 'file_denoise_Nr0.66.mp3'."""
    match = re.search(r"Nr([0-9.]+)", filename)
    if match:
        raw_value = match.group(1).rstrip('.')
        try:
            return float(raw_value)
        except ValueError:
            return None
    return None


def compare_with_all(original_path):
    mp3_files = glob.glob("*.mp3")
    mp3_files = [file for file in mp3_files if os.path.basename(file) != os.path.basename(original_path)]

    if not mp3_files:
        print("No other MP3 files found for comparison.")
        return

    results = []

    for processed_path in mp3_files:
        mse, snr = process_audio(original_path, processed_path)
        nr = extract_nr_value(processed_path)
        results.append((processed_path, mse, snr, nr))
        print(f"\nComparing '{original_path}' with '{processed_path}':")
        print(f"MSE: {mse}")
        print(f"SNR (dB): {snr}")

    results = [r for r in results if r[3] is not None]  # Remove entries without an Nr value
    results.sort(key=lambda x: x[3])  # Sort by Nr value

    print("\nResults:" + f"{'-'*40}")
    best_match = max(results, key=lambda x: x[2]) if results else None
    if best_match:
        print("\nBest matching file based on SNR:")
        print(f"File: {best_match[0]}, MSE: {best_match[1]}, SNR: {best_match[2]}")

    print("\nAll files sorted by Nr value:")
    max_filename_length = max(len(file) for file, _, _, _ in results) if results else 20
    print(f"{'No.':<5} {'File':<{max_filename_length}} {'MSE':<15} {'SNR':<15} {'Nr':<10}")
    for i, (file, mse, snr, nr) in enumerate(results, 1):
        print(f"{i:<5} {file:<{max_filename_length}} {mse:<15.5f} {snr:<15.5f} {nr:<10.2f}")

    # Extract values
    nr_values = [r[3] for r in results]
    snr_values = [r[2] for r in results]
    mse_values = [r[1] for r in results]

    # Create plot with two Y-axes
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot SNR
    color_snr = 'tab:blue'
    ax1.set_xlabel('Noise Reduction Setting (Nr)')
    ax1.set_ylabel('SNR (dB)', color=color_snr)
    ax1.plot(nr_values, snr_values, color=color_snr, marker='o', label='SNR (dB)', linewidth=2)
    ax1.tick_params(axis='y', labelcolor=color_snr)

    # Highlight best SNR point
    if best_match:
        ax1.scatter([best_match[3]], [best_match[2]], color='red', zorder=5,
                    label=f"Best SNR: Nr={best_match[3]}, SNR={best_match[2]:.2f} dB")

    # Plot MSE on secondary axis
    ax2 = ax1.twinx()
    color_mse = 'tab:green'
    ax2.set_ylabel('MSE', color=color_mse)
    ax2.plot(nr_values, mse_values, color=color_mse, label='MSE', linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color_mse)

    # Combine legends
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='best')

    plt.title("SNR and MSE vs. Noise Reduction Setting (Nr)")
    plt.grid(True)
    fig.tight_layout()
    plt.show()



def main():
    parser = argparse.ArgumentParser(description="Compare an original MP3 file with all other MP3 files in the directory.")
    parser.add_argument("original", help="Path to the original MP3 file")

    args = parser.parse_args()

    if not os.path.isfile(args.original):
        print("Error: The specified original file does not exist.")
        return

    compare_with_all(args.original)
    print("\n\n\n")
if __name__ == "__main__":
    main()
