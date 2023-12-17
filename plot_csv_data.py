
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

def rolling_average_with_filtering(data, window_size, quantile_threshold):
    def trimmed_rolling_average(window):
        if len(window) < window_size:
            return np.nan
        else:
            lower_bound = np.quantile(window, quantile_threshold)
            upper_bound = np.quantile(window, 1 - quantile_threshold)
            filtered_values = window[(window >= lower_bound) & (window <= upper_bound)]
            return filtered_values.mean()
    return data.rolling(window=window_size, center=True).apply(trimmed_rolling_average, raw=True)

def main(csv_file):
    # Load the data
    data = pd.read_csv(csv_file)

    # Applying the rolling average with filtering
    window_size = 20
    quantile_threshold = 0.1
    processed_data = data.apply(lambda col: rolling_average_with_filtering(col, window_size, quantile_threshold).iloc[::5])

    # Plotting all columns on the same chart
    plt.figure(figsize=(15, 10))
    for column in processed_data.columns:
        plt.plot(processed_data.index, processed_data[column], label=column)
    plt.title('Rolling Averages with Filtered Data')
    plt.xlabel('Data Index')
    plt.ylabel('Value')
    plt.legend()
    plt.show()

    # Calculating the ratios of Fp2/Fp1, T4/T3, and O2/O1
    ratios = pd.DataFrame()
    ratios['Fp2/Fp1'] = processed_data['Fp2'] / processed_data['Fp1']
    ratios['T4/T3'] = processed_data['T4'] / processed_data['T3']
    ratios['O2/O1'] = processed_data['O2'] / processed_data['O1']

    # Plotting the ratios
    plt.figure(figsize=(15, 10))
    for column in ratios.columns:
        plt.plot(ratios.index, ratios[column], label=column)
    plt.title('Ratios of Fp2/Fp1, T4/T3, and O2/O1')
    plt.xlabel('Data Index')
    plt.ylabel('Ratio Value')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file>")
    else:
        main(sys.argv[1])
