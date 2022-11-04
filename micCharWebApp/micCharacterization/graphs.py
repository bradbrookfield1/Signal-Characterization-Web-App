import sys
from matplotlib import pyplot as plt
from scipy import signal
import numpy as np
import librosa
import librosa.display
from .graphic_interfacing import get_graph

def get_signal(lib_list, dur_list):
    sig_chart_list = []
    if lib_list:
        for idx, lib_entry in enumerate(lib_list):
            plt.figure(1, figsize=(4, 3)).clf()
            librosa.display.waveshow(lib_entry[1], sr=lib_entry[0], max_points=sys.maxsize, offset=dur_list[idx][0])
            plt.title('Time Domain Original Signal')
            plt.xlabel('Time [s]')
            plt.ylabel('Amplitude')
            plt.tight_layout()
            sig_chart_list.append(get_graph())
    return sig_chart_list

def get_PSD(lib_list):    
    psd_chart_list = []
    if lib_list:
        for lib_entry in lib_list:            
            psd_freq, psd_data = signal.welch(x=lib_entry[1], fs=lib_entry[0])
            plt.figure(1, figsize=(4, 3)).clf()
            plt.loglog(psd_freq, psd_data, lw=1, label='Bruh')
            plt.title('Power Spectral Density')
            plt.xlabel('Frequency')
            plt.ylabel('PSD')
            plt.tight_layout()
            psd_chart_list.append(get_graph())
    return psd_chart_list

def get_spectrogram(lib_list):
    spec_chart_list = []
    if lib_list:
        for lib_entry in lib_list:
            spec_fft_data = librosa.stft(lib_entry[1])
            spec_fft_db_data = librosa.amplitude_to_db(abs(spec_fft_data), ref=np.max)
            plt.figure(1, figsize=(4, 3)).clf()
            librosa.display.specshow(
                spec_fft_db_data,
                sr=lib_entry[0],
                x_axis='time',
                y_axis='log',
            )
            plt.colorbar(format='%+2.f dB')
            plt.title('Spectrogram')
            plt.tight_layout()
            spec_chart_list.append(get_graph())
    return spec_chart_list

def get_PS(lib_list):
    return

def get_autocorrelation(lib_list):
    autocorr_chart_list = []
    if lib_list:
        for lib_entry in lib_list:
            autocorr_data = librosa.autocorrelate(lib_entry[1])
            plt.figure(1, figsize=(4, 3)).clf()
            plt.plot(autocorr_data)
            plt.title('Autocorrelation')
            plt.xlabel('Lag (frames)')
            plt.tight_layout()
            autocorr_chart_list.append(get_graph())
    return autocorr_chart_list

def get_percussive(lib_list):
    perc_chart_list = []
    if lib_list:
        for lib_entry in lib_list:
            spec_fft_data = librosa.stft(lib_entry[1])
            harm, perc = librosa.decompose.hpss(spec_fft_data)
            perc_db_data = librosa.amplitude_to_db(np.abs(perc), ref=np.max(np.abs(spec_fft_data)))
            plt.figure(1, figsize=(4, 3)).clf()
            librosa.display.specshow(
                perc_db_data,
                sr=lib_entry[0],
                x_axis='time',
                y_axis='log',
            )
            plt.colorbar(format='%+2.f dB')
            plt.title('Percussive Components')
            plt.tight_layout()
            perc_chart_list.append(get_graph())
    return perc_chart_list

def get_harmonic(lib_list):
    harm_chart_list = []
    if lib_list:
        for lib_entry in lib_list:
            spec_fft_data = librosa.stft(lib_entry[1])
            harm, perc = librosa.decompose.hpss(spec_fft_data)
            harm_db_data = librosa.amplitude_to_db(np.abs(harm), ref=np.max(np.abs(spec_fft_data)))
            plt.figure(1, figsize=(4, 3)).clf()
            librosa.display.specshow(
                harm_db_data,
                sr=lib_entry[0],
                x_axis='time',
                y_axis='log',
            )
            plt.colorbar(format='%+2.f dB')
            plt.title('Harmonic Components')
            plt.tight_layout()
            harm_chart_list.append(get_graph())
    return harm_chart_list

def get_harmonic_transform(lib_list):
    return