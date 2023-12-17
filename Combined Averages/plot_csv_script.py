
import pandas as pd
import matplotlib.pyplot as plt
import sys

def plot_csv(file_path):
    # Load the data from the CSV file
    data = pd.read_csv(file_path)

    # Selecting the first ten columns
    first_ten_columns = data.columns[:10]

    # Plotting
    plt.figure(figsize=(12, 8))

    # Plotting the first ten columns with 50% transparency and thinner black lines
    for column in first_ten_columns:
        plt.plot(data[column], color='black', alpha=0.5, linewidth=1)

    # Plotting the "Control" column as a thick black line
    plt.plot(data['Control'], color='black', linewidth=2)

    plt.title('Complexity Score Timeseries - Meditations vs Control')
    plt.xlabel('Time')
    plt.ylabel('Complexity')
    plt.grid(False)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <csv_file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    plot_csv(file_path)
