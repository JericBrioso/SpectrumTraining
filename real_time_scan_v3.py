import adi
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Sweep Parameters
START_FREQ = 300e6     # 300 MHz
STOP_FREQ = 800e6      # 800 MHz
STEP_FREQ = 5e6        # 5 MHz step
FFT_SIZE = 64
SWEEP_DELAY = 0.1      # seconds

# SDR Parameters
SAMPLE_RATE = 2e6
BANDWIDTH = 20e6
GAIN = 30

# Frequency sweep points
center_freqs = np.arange(START_FREQ, STOP_FREQ + STEP_FREQ, STEP_FREQ)

# Initialize SDR
sdr = adi.Pluto("ip:192.168.2.100")
sdr.rx_sample_rate = int(SAMPLE_RATE)
sdr.rx_rf_bandwidth = int(BANDWIDTH)
sdr.rx_gain_control_mode = "manual"
sdr.rx_hardwaregain = GAIN

# Plot setup
fig, ax = plt.subplots()
combined_span = SAMPLE_RATE * len(center_freqs)  # Total width in Hz
total_bins = FFT_SIZE * len(center_freqs)
x_data = np.linspace(START_FREQ, STOP_FREQ, total_bins) / 1e6  # In MHz
line, = ax.plot(x_data, np.zeros_like(x_data))

ax.set_title("Wideband Spectrum: 300 MHz – 800 MHz")
ax.set_xlabel("Frequency (MHz)")
ax.set_ylabel("Power (dB)")
ax.set_ylim(-100, 50)
ax.set_xlim(x_data[0], x_data[-1])
ax.grid(True)

# Animation update function
def update(frame):
    full_spectrum = []

    for cf in center_freqs:
        sdr.rx_lo = int(cf)
        samples = sdr.rx()
        if len(samples) < FFT_SIZE:
            spectrum = np.zeros(FFT_SIZE)
        else:
            windowed = samples[:FFT_SIZE] * np.hanning(FFT_SIZE)
            spectrum = 20 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(windowed))) + 1e-10)
            spectrum[0] = np.nan
            spectrum[-1] = np.nan
        full_spectrum.extend(spectrum)

    # Update plot
    line.set_ydata(full_spectrum)
    return line,

# Start animation
ani = animation.FuncAnimation(fig, update, interval=SWEEP_DELAY * 1000)
plt.show()

# Cleanup
sdr.rx_destroy_buffer()

