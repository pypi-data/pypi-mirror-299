import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import os

class eyediagram:
    def __init__(self, data):
        if 'Volt' not in data.columns:
            raise ValueError("The dataset does not contain the required 'Volt' column.")
        self.data = data
        self.voltages_ac = self.calculate_ac_voltages()

    def calculate_ac_voltages(self):
        # Subtract the mean to get AC voltages
        return np.array(self.data['Volt'] - np.mean(self.data['Volt']))  # Ensure numpy array

    def find_samples_per_symbol(self):
        # Find peaks in the signal to estimate the symbol period
        peaks, _ = find_peaks(self.voltages_ac)

        if len(peaks) < 2:
            raise ValueError("Not enough peaks to calculate samples per symbol.")

        periods_between_peaks = np.diff(peaks)  # Calculate the periods between detected peaks
        samples_per_symbol = int(0.5 * np.median(periods_between_peaks))

        if samples_per_symbol <= 0:
            raise ValueError("Calculated samples per symbol is not valid.")

        return samples_per_symbol

    def find_offset(self):
        # Find the first negative-to-positive zero-crossing in the AC signal
        for i in range(len(self.voltages_ac) - 1):
            if self.voltages_ac[i] < 0 and self.voltages_ac[i + 1] >= 0:
                return i
        return 0  # Default to 0 if no zero-crossing found

    def plot(self, n, offset, file_name):
        # Offset the data
        data_offset = self.voltages_ac[offset:]
        num_samples = len(data_offset)
        num_symbols = num_samples // n  # Calculate number of symbols

        if num_symbols <= 0:
            print("Not enough data to plot the eye diagram.")
            return

        # Truncate data to fit the reshape operation
        truncated_data = data_offset[:num_symbols * n]

        # Ensure the length of truncated data matches the required shape
        if len(truncated_data) != num_symbols * n:
            print(f"Mismatch in truncating data. Expected {num_symbols * n} samples, got {len(truncated_data)} samples.")
            return

        # Reshape the truncated data and plot the eye diagram
        reshaped_voltages = np.reshape(truncated_data, (num_symbols, n))

        # Plot the eye diagram
        plt.figure(figsize=(10, 6))
        for i in range(num_symbols):
            plt.plot(reshaped_voltages[i], color='blue', alpha=0.3)
        plt.title('Eye Diagram')
        plt.xlabel('Sample Number')
        plt.ylabel('Voltage (V)')
        plt.grid(True)

        # Save the figure using the file name
        figure_name = f"{os.path.splitext(file_name)[0]}_eye_diagram.png"
        plt.savefig(figure_name)
        plt.show()
        print(f"Eye diagram saved as {figure_name}")

        # Save the reshaped eye diagram data to a CSV file
        csv_file_name = f"{os.path.splitext(file_name)[0]}_eye_diagram.csv"
        pd.DataFrame(reshaped_voltages).to_csv(csv_file_name, index=False)
        print(f"Eye diagram data saved as {csv_file_name}")
