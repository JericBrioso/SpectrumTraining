import numpy as np

# Load the CSV file (skip the header row)
data = np.loadtxt("rx_samples.csv", delimiter=",", skiprows=1)

# Reconstruct complex samples
rx_samples = data[:, 0] + 1j * data[:, 1]

print(rx_samples[0:10])
