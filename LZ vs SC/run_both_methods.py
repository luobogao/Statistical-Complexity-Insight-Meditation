import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import detrend
import argparse
from tqdm import tqdm
from lempel_ziv_complexity import lempel_ziv_complexity
from copy import deepcopy
import sys
import csv
from statistical_complexity import *

# Global variables
COLUMNS = ['F7', 'Fp1', 'Fp2', 'F8', 'F3', 'Fz', 'F4', 'C3', 'Cz', 'P8', 'P7', 'Pz', 'P4', 'T3', 'P3', 'O1', 'O2', 'C4', 'T4']
#COLUMNS = ["AF8", "AF7", "TP10", "TP9"]
SAMPLE_RATE = 500  # Hz
WINDOW_SIZE = 30  # seconds for both LZ and SC complexity
STEP_SIZE = 10  # seconds for both LZ and SC complexity

# Statistical Complexity Parameters
LAMBDA = 7  ## the memory length
SIGMA = 0.01

LZ_ADJUST = 50

def calculate_lz(signal):
    # Linear Detrending
    signal = detrend(signal)

    # Baseline Subtraction
    signal -= np.mean(signal)

    # Normalization of Standard Deviation
    signal /= np.std(signal)

    # Binarization based on median
    median_value = np.median(signal)
    signal = np.where(signal >= median_value, 1, 0)

    # Complexity Analysis (number of 0-1 transitions)
    #complexity = np.sum(np.abs(np.diff(signal)))
    # Convert signal to string format for LZ complexity calculation
    signal_str = ''.join(map(str, signal))
    complexity = lempel_ziv_complexity(signal_str)
 
    return complexity

def sliding_window_process(data, window_size, overlap, sample_rate):
    """
    Apply a sliding window on the data.
    """
    windowed_data = []
    step_size = window_size - overlap
    num_samples = window_size * sample_rate

    for start in range(0, len(data) - num_samples + 1, step_size * sample_rate):
        windowed_data.append(data[start:start + num_samples])

    return windowed_data


def read_csv_columns(file_path, column_names):
    """
    Read specified columns from a CSV file.
    """
    try:
        data = pd.read_csv(file_path, usecols=column_names)
        return data
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)    


def combined_process_eeg_data(file_path):
    # Load EEG data
    eeg_data = pd.read_csv(file_path)

    # Prepare for sliding window analysis
    window_length_samples = WINDOW_SIZE * SAMPLE_RATE
    step_length_samples = STEP_SIZE * SAMPLE_RATE

    # Prepare DataFrames for saving complexities
    lz_complexity_df = pd.DataFrame()
    sc_complexity_df = pd.DataFrame()

    # Process each column
    for column in tqdm(COLUMNS, desc="Processing EEG Columns"):
        lz_complexity_values = []
        sc_complexity_values = []
        time_stamps = []

        for start in range(0, len(eeg_data) - window_length_samples + 1, step_length_samples):
            end = start + window_length_samples
            window_signal = eeg_data[column].iloc[start:end]
                        
            if window_signal.isna().any():
            # Add NaN to complexity lists and continue
                lz_complexity_values.append(np.nan)
                sc_complexity_values.append(np.nan)
                time_stamps.append(start / SAMPLE_RATE)
                continue

            # Lempel-Ziv Complexity
            lz_complexity = calculate_lz(window_signal.values)
            lz_complexity_values.append(lz_complexity)

            # Statistical Complexity
            binary_string = binarise(window_signal.values)
            sc_complexity = calculate(binary_string, LAMBDA, SIGMA)
            sc_complexity_values.append(sc_complexity)

            time_stamps.append(start / SAMPLE_RATE)

        lz_complexity_df[column] = lz_complexity_values
        sc_complexity_df[column] = sc_complexity_values

    # Plotting LZ Complexity
    plt.figure(figsize=(12, 6))
    for column in COLUMNS:
        plt.plot(time_stamps, lz_complexity_df[column], label=column)
    plt.xlabel('Time (seconds)')
    plt.ylabel('LZ Complexity')
    plt.title('EEG Signal LZ Complexity Over Time')
    plt.legend()
    plt.grid(True)
    #plt.show()

    # Plotting SC Complexity
    plt.figure(figsize=(12, 6))
    for column in COLUMNS:
        plt.plot(time_stamps, sc_complexity_df[column], label=column)
    plt.xlabel('Time (seconds)')
    plt.ylabel('SC Complexity')
    plt.title('EEG Signal SC Complexity Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Save complexities to CSV
    combined_complexity_df = pd.DataFrame()
    combined_complexity_df['Time'] = time_stamps
    ##lz_complexity_df.round(3).to_csv(file_path.replace('.csv', '_lz.csv'), index=False)
    ##sc_complexity_df.round(3).to_csv(file_path.replace('.csv', '_sc.csv'), index=False)
    # Number of steps in each rolling window
    rolling_steps = 10

    
    # Apply rolling mean
    for column in COLUMNS:
        combined_complexity_df[column + '_LZ'] = lz_complexity_df[column].rolling(rolling_steps, min_periods=1).mean().tolist()
        # normalize
        combined_complexity_df[column + '_LZ'] = combined_complexity_df[column + '_LZ'] / LZ_ADJUST
    for column in COLUMNS:
        combined_complexity_df[column + '_SC'] = sc_complexity_df[column].rolling(rolling_steps, min_periods=1).mean().tolist()

    combined_complexity_df.round(3).to_csv(file_path.replace('.csv', '_combined_complexity.csv'), index=False)


def main():
    parser = argparse.ArgumentParser(description="Process EEG data from a CSV file.")
    parser.add_argument("file_path", help="Path to the CSV file")
    args = parser.parse_args()

    combined_process_eeg_data(args.file_path)

if __name__ == "__main__":
    main()
