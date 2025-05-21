import adi
import numpy as np
import matplotlib.pyplot as plt
import time

# Pluto SDR configuration
pluto = adi.Pluto()
pluto.sample_rate = int(2.4e6)  # 2.4 MS/s
pluto.rx_rf_bandwidth = int(2e6)  # 2 MHz RF bandwidth
pluto.rx_lo = int(100e6)  # Start at 100 MHz

# Frequency scan parameters
start_freq = int(100e6)
stop_freq = int(1000e6)
step_freq = int(10e6)  # 10 MHz steps
num_samples = 2048

# Setup plot
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_ylim(-100, 0)
ax.set_xlim(0, pluto.sample_rate)
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Power (dB)")

try:
    while True:
        for freq in range(start_freq, stop_freq, step_freq):
            pluto.rx_lo = freq
            time.sleep(0.1)  # Allow LO to settle

            samples = pluto.rx()
            fft_data = np.fft.fftshift(np.fft.fft(samples, n=num_samples))
            power = 20 * np.log10(np.abs(fft_data) + 1e-10)

            freqs = np.fft.fftshift(np.fft.fftfreq(num_samples, 1 / pluto.sample_rate))

            line.set_ydata(power)
            line.set_xdata(freqs)
            ax.set_xlim(freqs[0], freqs[-1])
            ax.set_title(f"Center Frequency: {freq / 1e6:.1f} MHz")
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(1)  # Refresh interval

except KeyboardInterrupt:
    print("Frequency scanning interrupted by user.")
finally:
    pluto.rx_destroy_buffer()
    plt.ioff()
    plt.show()
