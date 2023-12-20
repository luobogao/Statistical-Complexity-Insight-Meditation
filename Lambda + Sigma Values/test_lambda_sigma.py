import pandas as pd
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import detrend
import sys
import argparse
from statistical_complexity import *

# Hardcoded column
COLUMN = 'AF8'

# Global variables
SAMPLE_RATE = 256  # Hz
WINDOW_SIZE = 60  # seconds for SC complexity
STEP_SIZE = 20  # seconds for SC complexity

lambda_low = 10
lambda_high = 12

sigma_low = 0.01
sigma_high = 0.02

def calculate_sc(signal, lambda_, sigma_):
    # Statistical Complexity Calculation
    binary_string = binarise(signal)
    return calculate(binary_string, lambda_, sigma_)

def sliding_window_process(data, window_size, overlap, sample_rate):
    # Apply a sliding window on the data.
    windowed_data = []
    step_size = window_size - overlap
    num_samples = window_size * sample_rate

    for start in range(0, len(data) - num_samples + 1, step_size * sample_rate):
        windowed_data.append(data[start:start + num_samples])

    return windowed_data

def read_csv_column(file_path, column_name):
    # Read a single column from a CSV file.
    try:
        data = pd.read_csv(file_path, usecols=[column_name])
        return data
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)    

def process_eeg_data(file_path):
    # Load EEG data
    eeg_data = read_csv_column(file_path, COLUMN)

    # Prepare for sliding window analysis
    window_length_samples = WINDOW_SIZE * SAMPLE_RATE
    step_length_samples = STEP_SIZE * SAMPLE_RATE

    plt.figure(figsize=(12, 6))

    # DataFrame to store complexity values for each lambda and sigma
    complexity_df = pd.DataFrame()

    # Iterate over lambda and sigma values
    for lambda_ in tqdm(range(lambda_low, lambda_high), desc="Lambda values"):  # lambda from 2 to 7    
        for sigma_ in np.arange(sigma_low, sigma_high, 0.01):  # sigma from 0.01 to 0.1
            sc_complexity_values = []
            time_stamps = []

            for start in range(0, len(eeg_data) - window_length_samples + 1, step_length_samples):
                end = start + window_length_samples
                window_signal = eeg_data[COLUMN].iloc[start:end]
                        
                if window_signal.isna().any():
                    sc_complexity_values.append(np.nan)
                    continue

                # Statistical Complexity
                sc_complexity = calculate_sc(window_signal.values, lambda_, sigma_)
                sc_complexity_values.append(sc_complexity)

            # Accumulate data for plotting and CSV
            complexity_df[f'Lambda_{lambda_}_Sigma_{sigma_}'] = sc_complexity_values
            plt.plot(range(len(sc_complexity_values)), sc_complexity_values, label=f'Lambda={lambda_}, Sigma={sigma_}')

    # Plotting SC Complexity for all combinations of lambda and sigma
    plt.xlabel('Time (seconds)')
    plt.ylabel('SC Complexity')
    plt.title('EEG Signal SC Complexity Over Time for Various Lambda and Sigma')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Save to CSV
    output_filename = file_path.replace('.csv', '_combos.csv')
    complexity_df.to_csv(output_filename, index=False)
    print(f"Saved complexity data to {output_filename}")

def main():
    parser = argparse.ArgumentParser(description="Process EEG data for statistical complexity.")
    parser.add_argument("file_path", help="Path to the EEG CSV file")
    args = parser.parse_args()

    process_eeg_data(args.file_path)

if __name__ == "__main__":
    main()
