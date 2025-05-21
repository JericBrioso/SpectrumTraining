import numpy as np
import adi
from scipy.io.wavfile import write

# SDR config
sample_rate = 1e6      # Hz
center_freq = 500e6    # Hz
num_samps = 1_000_000  # total samples to save (~1 second at 1 MSPS)

sdr = adi.Pluto("ip:192.168.2.100")
sdr.sample_rate = int(sample_rate)
sdr.rx_lo = int(center_freq)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = 4096
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 0.0

# Clear initial buffer
for _ in range(5):
    sdr.rx()

print("Capturing samples...")

# Collect samples in chunks
samples = []
samples_needed = num_samps
while samples_needed > 0:
    chunk = sdr.rx()
    samples.append(chunk)
    samples_needed -= len(chunk)

samples = np.concatenate(samples)[:num_samps]
print(f"Captured {len(samples)} complex samples.")

# Normalize and convert to 16-bit PCM
max_val = np.max(np.abs(samples))
samples /= max_val + 1e-12  # normalize to -1.0 to 1.0 range
iq_stereo = np.stack((samples.real, samples.imag), axis=-1)  # shape: (N, 2)
iq_int16 = np.int16(iq_stereo * 32767)

# Save to WAV
wav_filename = "sdr_capture.wav"
write(wav_filename, int(sample_rate), iq_int16)
print(f"Saved to {wav_filename}")
