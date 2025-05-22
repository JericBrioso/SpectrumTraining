import numpy as np
import adi
import time
import csv

# SDR and sweep settings
sample_rate = 1e6        # Hz
num_samps = 1024         # Samples per capture
start_freq = 100e6       # 100 MHz
stop_freq = 1000e6       # 1000 MHz
step_freq = 10e6         # Frequency step (10 MHz)
capture_interval = 0.1   # Seconds between captures

# Initialize SDR
sdr = adi.Pluto("ip:192.168.2.100")
sdr.gain_control_mode_chan0 = "manual"
sdr.rx_hardwaregain_chan0 = 70.0
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps

# Frequency list
freqs = np.arange(start_freq, stop_freq + step_freq, step_freq)

# Continuous sweeping loop
capture_count = 0
# Data storage
all_samples = []
try:
    while True:
        for freq in freqs:
            sdr.rx_lo = int(freq)
            time.sleep(0.05)  # Allow time for LO to settle

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
