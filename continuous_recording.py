import numpy as np
import adi
import time
import csv

sample_rate = 1e6  # Hz
num_samps = 128  # samples per read
start_freq = 1e6  # 1 MHz
end_freq = 1000e6  # 1000 MHz
step_time = 0.1  # seconds

# Create SDR object
sdr = adi.Pluto('ip:192.168.2.100')
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 70.0  # dB
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps

# Data storage
all_samples = []

try:
    for freq in np.arange(start_freq, end_freq + 1, sample_rate):
        sdr.rx_lo = int(freq)
        time.sleep(step_time)

        rx_samples = sdr.rx()
        freq_MHz = freq / 1e6

        # Add samples with frequency info
        for sample in rx_samples:
            all_samples.append([freq_MHz, sample.real, sample.imag])

        print(f"Collected {len(rx_samples)} samples at {freq_MHz:.1f} MHz")

except KeyboardInterrupt:
    print("Sweep interrupted by user.")

# Save all data to one CSV
with open("rx_samples_combined.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Frequency_MHz", "Real", "Imag"])
    writer.writerows(all_samples)

print("Saved all samples to rx_samples_combined.csv")

# Clean up
del sdr
