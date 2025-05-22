import adi
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# Sweep Parameters
START_FREQ = 300e6     # 300 MHz
STOP_FREQ = 800e6      # 800 MHz
STEP_FREQ = 1e6        # 1 MHz step for overlap (less than SAMPLE_RATE)
FFT_SIZE = 64         # Higher resolution
SWEEP_DELAY = 0.2      # Seconds between updates

# SDR Parameters
SAMPLE_RATE = 2e6      # Match RF bandwidth
GAIN = 0              # dB

# Frequency sweep points
center_freqs = np.arange(START_FREQ, STOP_FREQ + STEP_FREQ, STEP_FREQ)

# Initialize PlutoSDR
sdr = adi.Pluto("ip:192.168.2.100")
sdr.rx_sample_rate = int(SAMPLE_RATE)
sdr.rx_rf_bandwidth = int(SAMPLE_RATE)  # Match to sample rate to avoid aliasing
sdr.rx_gain_control_mode = "manual"
sdr.rx_hardwaregain = GAIN
sdr.rx_buffer_size = 128               # More samples for FFT slicing

# FFT window
window = np.hanning(FFT_SIZE)
window_gain = np.sum(window)

# Plot setup
fig, ax = plt.subplots()
total_bins = FFT_SIZE * len(center_freqs)
x_data = np.linspace(START_FREQ, STOP_FREQ, total_bins) / 1e6  # MHz
line, = ax.plot(x_data, np.zeros_like(x_data))

ax.set_title("Real-time Spectrum Scanning")
ax.set_xlabel("Frequency (MHz)")
ax.set_ylabel("Power (dB)")
ax.set_ylim(-100, 100)
ax.set_xlim(x_data[0], x_data[-1])
ax.grid(True)

# Animation update function
def update(frame):
    full_spectrum = []

    for cf in center_freqs:
        sdr.rx_lo = int(cf)
        time.sleep(0.01)  # Allow PLL to settle
        samples = sdr.rx()

        if len(samples) < FFT_SIZE:
            spectrum = np.full(FFT_SIZE, -120.0)
        else:
            windowed = samples[:FFT_SIZE] * window
            fft_out = np.fft.fftshift(np.fft.fft(windowed))
            fft_mag = np.abs(fft_out) / window_gain
            spectrum = 20 * np.log10(fft_mag + 1e-10)

        full_spectrum.extend(spectrum)

    line.set_ydata(full_spectrum)
    return line,

# Start animation
ani = animation.FuncAnimation(fig, update, interval=SWEEP_DELAY * 1000)
plt.show()

# Cleanup
sdr.rx_destroy_buffer()
del sdr
