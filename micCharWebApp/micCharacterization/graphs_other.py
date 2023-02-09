import math
from matplotlib import pyplot as plt
from scipy import signal
from functools import partial
import numpy as np
import librosa
import librosa.display
from .graphic_interfacing import get_graph, get_abs_coeff_graph
from .calculations import calc_coeff

fig_size = (6, 4.5)

def get_pure_SNR(sig_list, noise_list, name, mic_Data_Record):
    sig_freq, sig_data = signal.welch(x=sig_list[1], fs=sig_list[0])
    noise_freq, noise_data = signal.welch(x=noise_list[1], fs=noise_list[0])
    snr_data = []
    db_data = []
    for sig, noise in zip(sig_data, noise_data):
        this_ratio = sig/noise
        snr_data.append(this_ratio)
        db_data.append(10*math.log10(this_ratio))
    plt.figure(1, figsize=fig_size).clf()
    plt.plot(sig_freq, db_data, label='', lw=1, alpha=0.75)
    plt.title(name + '\nSNR Given Signal and Noise')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('SNR (dB)')
    plt.grid(True)
    plt.tight_layout()
    return get_graph('Spectral Graphs', 'pure_Signal_SNR_Graph', mic_Data_Record)

def get_SNR_gvn_sig(noisy_sig_list, sig_list, name, mic_Data_Record):
    noisy_sig_freq, noisy_sig_data = signal.welch(x=noisy_sig_list[1], fs=noisy_sig_list[0])
    sig_freq, sig_data = signal.welch(x=sig_list[1], fs=sig_list[0])
    snr_data = []
    db_data = []
    for noisy_sig, sig in zip(noisy_sig_data, sig_data):
        this_ratio = 1/(((noisy_sig*1.25)/sig) - 1)
        snr_data.append(this_ratio)
        db_data.append(10*math.log10(this_ratio))
    plt.figure(1, figsize=fig_size).clf()
    plt.plot(noisy_sig_freq, db_data, label='', lw=1, alpha=0.75)
    plt.title(name + '\nSNR Given Signal')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('SNR (dB)')
    plt.grid(True)
    plt.tight_layout()
    return get_graph('Spectral Graphs', 'given_Signal_SNR_Graph', mic_Data_Record)

def get_SNR_gvn_noise(noisy_sig_list, noise_list, name, mic_Data_Record):
    noisy_sig_freq, noisy_sig_data = signal.welch(x=noisy_sig_list[1], fs=noisy_sig_list[0], average='mean')
    noise_freq, noise_data = signal.welch(x=noise_list[1], fs=noise_list[0], average='mean')
    snr_data = []
    db_data = []
    for noisy_sig, noise in zip(noisy_sig_data, noise_data):
        this_ratio = ((noisy_sig*1.25)/noise) - 1
        snr_data.append(this_ratio)
        db_data.append(10*math.log10(this_ratio))
    plt.figure(1, figsize=fig_size).clf()
    plt.plot(noisy_sig_freq, db_data, label='', lw=1, alpha=0.75)
    plt.title(name + '\nSNR Given Noise')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('SNR (dB)')
    plt.grid(True)
    plt.tight_layout()
    return get_graph('Spectral Graphs', 'given_Noise_SNR_Graph', mic_Data_Record)

def get_SNR_system(noisy_sig_list, sig_list, name, mic_Data_Record):
    noisy_sig_freq, noisy_sig_data = signal.welch(x=noisy_sig_list[1], fs=noisy_sig_list[0])
    sig_freq, sig_data = signal.welch(x=sig_list[1], fs=sig_list[0])
    noise_data = noisy_sig_data - sig_data
    snr_data = []
    db_data = []
    for sig, noise in zip(sig_data, noise_data):
        this_ratio = sig/noise
        snr_data.append(this_ratio)
        db_data.append(10*math.log10(this_ratio))
    plt.figure(1, figsize=fig_size).clf()
    plt.plot(noisy_sig_freq, db_data, label='', lw=1, alpha=0.75)
    plt.title(name + '\nSNR System Approach')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('SNR (ratio)')
    plt.grid(True)
    plt.tight_layout()
    return get_graph('Spectral Graphs', 'system_Signal_SNR_Graph', mic_Data_Record)

def get_spec_prop_abs_coeff_hum(freqs, distance, temperature, rel_hum_array, p_bar, p_ref):
    rel_hum_abs_coeff = []
    for rel_hum in rel_hum_array:
        rel_hum_abs_coeff.append(calc_coeff(freqs, distance, temperature, rel_hum, p_bar, p_ref))
    plt.figure(1, figsize=fig_size).clf()
    plt.title('Spectral Sound Absorption Coefficient\nVarying Relative Humidity')
    plt.xlabel(r'Frequency/Pressure $\left(\frac{Hz}{atm}\right)$')
    plt.ylabel(r'Absorption Coefficient $\left(\frac{dB}{m \cdot atm}\right)$')
    plt.grid(True)
    for i in range(len(rel_hum_abs_coeff)):
        plt.loglog(freqs, rel_hum_abs_coeff[i], label=str(rel_hum_array[i]*100) + ' %', lw=0.75, alpha=0.75)
    plt.legend()
    plt.tight_layout()
    return get_abs_coeff_graph()

def get_spec_prop_abs_coeff_temp(freqs, distance, temp_array, relative_humidity, p_bar, p_ref):
    temp_abs_coeff = []
    for temp in temp_array:
        temp_abs_coeff.append(calc_coeff(freqs, distance, temp, relative_humidity, p_bar, p_ref))
    plt.figure(1, figsize=fig_size).clf()
    plt.title('Spectral Sound Absorption Coefficient\nVarying Temperature')
    plt.xlabel(r'Frequency/Pressure $\left(\frac{Hz}{atm}\right)$')
    plt.ylabel(r'Absorption Coefficient $\left(\frac{dB}{m \cdot atm}\right)$')
    plt.grid(True)
    for i in range(len(temp_abs_coeff)):
        plt.loglog(freqs, temp_abs_coeff[i], label=str(temp_array[i] - 273.15) + ' C', lw=0.75, alpha=0.75)
    plt.legend()
    plt.tight_layout()
    return get_abs_coeff_graph()

def get_spec_prop_abs_coeff_dist(freqs, dist_array, temperature, relative_humidity, p_bar, p_ref):
    dist_abs_coeff = []
    for dist in dist_array:
        dist_abs_coeff.append(calc_coeff(freqs, dist, temperature, relative_humidity, p_bar, p_ref))
    plt.figure(1, figsize=fig_size).clf()
    plt.title('Spectral Sound Absorption Coefficient\nVarying Distance')
    plt.xlabel(r'Frequency/Pressure $\left(\frac{Hz}{atm}\right)$')
    plt.ylabel(r'Absorption Coefficient $\left(\frac{dB}{\_\_\_\_ m \cdot atm}\right)$')
    plt.grid(True)
    for i in range(len(dist_abs_coeff)):
        plt.loglog(freqs, dist_abs_coeff[i], label=str(dist_array[i]) + ' m', lw=0.75, alpha=0.75)
    plt.legend()
    plt.tight_layout()
    return get_abs_coeff_graph()