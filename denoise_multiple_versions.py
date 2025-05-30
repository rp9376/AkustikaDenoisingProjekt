import argparse
from denoiser import denoise_audio

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Denoise an audio file.")
    parser.add_argument("input", help="Path to input audio file.")
    parser.add_argument("--output", help="Name of the output denoised audio file.")
    parser.add_argument("--var", type=int, default=11, help="Number of variations to create.")

    
    args = parser.parse_args()

    for i in range(1, args.var+1):  # Start from 1 to skip denoising value 0
        noise_reduction = round(i / (args.var), 4) if args.var > 1 else 0
        
        output_file = f"{i}_{args.output}_Nr{noise_reduction}.mp3" if args.output else f"{i}_denoise_Nr{noise_reduction}.mp3"
        
        denoise_audio(args.input, output_file, noise_reduction)