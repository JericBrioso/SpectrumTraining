import numpy as np
import adi
import matplotlib.pyplot as plt

# Load the CSV file (skip the header row)
data = np.loadtxt("rx_samples.csv", delimiter=",", skiprows=1)

# Reconstruct complex samples
rx_samples = data[:, 0] + 1j * data[:, 1]

sample_rate = 1e6 # Hz
center_freq = 100e6 # Hz
num_samps = len(rx_samples) #1024
print(rx_samples[0:10])

#downsampling
downsample = 512
rx_samples_down = rx_samples[::(num_samps//downsample)]
print(rx_samples_down[0:10])


# Calculate power spectral density (frequency domain version of original signal)
psd = np.abs(np.fft.fftshift(np.fft.fft(rx_samples)))**2
psd_dB = 10*np.log10(psd)
f = np.linspace(sample_rate/-2, sample_rate/2, len(psd))

# Calculate power spectral density (frequency domain version of downsamopled signal)
psd_down = np.abs(np.fft.fftshift(np.fft.fft(rx_samples_down)))**2
psd_dB_down = 10*np.log10(psd_down)
f_down = f[::(num_samps//downsample)]


# Plot freq domain
plt.figure(1)
plt.subplot(2,1,1)
plt.plot(f/1e6, psd_dB)
plt.xlabel("Frequency [MHz]")
plt.ylabel("PSD_original")

plt.subplot(2,1,2)
plt.plot(f_down/1e6, psd_dB_down)
plt.xlabel("Frequency [MHz]")
plt.ylabel("PSD_down")

plt.show()
