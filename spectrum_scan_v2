import numpy as np
import adi
import matplotlib.pyplot as plt
import time

# Sweep config
start_freq = 300e6
stop_freq = 800e6
step_freq = 1e6
sample_rate = 1e6
num_samps = 1024
update_interval = 1  # seconds between full sweep updates

# Initialize SDR
sdr = adi.Pluto("ip:192.168.2.100")
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 0.0

# Sweep frequency list
sweep_freqs = np.arange(start_freq, stop_freq + step_freq, step_freq)

# Set up plot
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], '.-', markersize=2)
ax.set_title("Real-Time Spectrum Sweep (300–800 MHz)")
ax.set_xlabel("Frequency [MHz]")
ax.set_ylabel("Power [dBm]")
ax.set_xlim(start_freq / 1e6, stop_freq / 1e6)
ax.set_ylim(-120, 0)
plt.grid(True)

while True:
    sweep_result_freqs = []
    sweep_result_psd = []

    for center_freq in sweep_freqs:
        sdr.rx_lo = int(center_freq)
        time.sleep(0.03)  # Let LO settle briefly

        # Clear buffer
        for _ in range(2):
            sdr.rx()

        # Get samples
        rx_samples = sdr.rx()
        fft_vals = np.fft.fftshift(np.fft.fft(rx_samples))
        psd = np.abs(fft_vals)**2 / num_samps
        psd_dBm = 10 * np.log10(psd + 1e-12)

        # Absolute frequency axis
        freqs = np.linspace(-sample_rate / 2, sample_rate / 2, num_samps) + center_freq
        sweep_result_freqs.extend(freqs / 1e6)  # Convert to MHz
        sweep_result_psd.extend(psd_dBm)

    # Update plot
    line.set_data(sweep_result_freqs, sweep_result_psd)
    ax.relim()
    ax.autoscale_view(scalex=False)  # Don’t autoscale x (fixed sweep range)
    plt.draw()
    plt.pause(0.01)

    time.sleep(update_interval - 0.01)  # maintain ~1 sec update rate
