import numpy as np
import adi
import matplotlib.pyplot as plt

sample_rate = 1e6 # Hz
center_freq = 100e6 # Hz
num_samps = 128 # number of samples returned per call to rx()

sdr = adi.Pluto('ip:192.168.2.100')
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 70.0 # dB
sdr.rx_lo = int(center_freq)
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate) # filter width, just set it to the same as sample rate for now
sdr.rx_buffer_size = num_samps

rx_samples = sdr.rx() # receive samples off Pluto
print(rx_samples[0:10])

#Exercise: save rx_samples in csv file.
# Save as CSV
np.savetxt("rx_samples.csv", np.column_stack((rx_samples.real, rx_samples.imag)), delimiter=",", header="Real,Imag", comments='')

