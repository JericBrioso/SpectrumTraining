import numpy as np
import adi
import time

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
try:
    while True:
        for freq in freqs:
            sdr.rx_lo = int(freq)
            time.sleep(0.05)  # Allow time for LO to settle

            rx_samples = sdr.rx()

            # Generate filename with count and frequency
            filename = f"rx_samples_{capture_count:05d}_{int(freq/1e6)}MHz.csv"

            # Save to CSV
            np.savetxt(filename,
                       np.column_stack((rx_samples.real, rx_samples.imag)),
                       delimiter=",", header="Real,Imag", comments='')

            print(f"[{capture_count}] Captured at {freq/1e6} MHz → Saved {filename}")
            capture_count += 1

            # Wait remaining time of capture interval
            time.sleep(max(0, capture_interval - 0.05))

except KeyboardInterrupt:
    print("Sweep stopped by user.")
