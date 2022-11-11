import math
from matplotlib import pyplot as plt
from scipy import signal
import numpy as np
import librosa
import librosa.display
from .graphic_interfacing import get_graph
from .calculations import fft_vectorized

width = 3.75
height = 2.8125
figsize = (width, height)
figsize_xl = (width*3, height)

def get_PSD(lib_list):    
    avg_chart_list = []
    if lib_list:
        for lib_entry in lib_list:            
            avg_freq, avg_data = signal.welch(x=lib_entry[1], fs=lib_entry[0])
            plt.figure(1, figsize=figsize).clf()
            plt.loglog(avg_freq, avg_data, lw=1, label='')
            plt.title('Power Spectral Density')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Power Spectral Density (V^2/Hz)')
            plt.grid(True)
            plt.tight_layout()
            avg_chart_list.append(get_graph())
    return avg_chart_list

def get_phase_spectrum(sig_list):
    phase_chart_list = []
    if sig_list:
        for sig_entry in sig_list:
            plt.figure(1, figsize=figsize).clf()
            freq, sig = sig_entry.phase_spectrum()
            plt.semilogx(freq, sig)
            plt.title('Phase Spectrum')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Phase (rad)')
            plt.grid(True)
            plt.tight_layout()
            phase_chart_list.append(get_graph())
    return phase_chart_list

def get_harmonic_prediction(lib_list, num_harm_list):
    num_harmonics = []
    for num_harm in num_harm_list:
        num_harmonics.append(num_harm if num_harm else 5)
    harm_fund_freq_preds = []
    if lib_list:
        for idx, lib_entry in enumerate(lib_list):
            tm = len(lib_entry[1])/lib_entry[0]
            pow_of_2 = math.floor(math.log2(len(lib_entry[1])))
            lib_time_data = signal.resample(lib_entry[1], 2**pow_of_2)
            new_sr = len(lib_time_data)/tm
            for r in range(1, num_harmonics[idx] + 1):
                if r == 1:
                    harm_preds_temp = np.array(fft_vectorized(lib_time_data, r))
                else:
                    harm_preds_temp = np.vstack((harm_preds_temp, fft_vectorized(lib_time_data, r)))
            harm_preds_temp = np.abs(harm_preds_temp)**(-1)
            harm_preds_temp = (np.sum(harm_preds_temp, axis=0)/num_harmonics[idx])**(-1)
            harm_preds_temp = librosa.amplitude_to_db(harm_preds_temp)
            freqs = librosa.fft_frequencies(sr=new_sr, n_fft=len(lib_time_data)*2)[1:]
            plt.figure(1, figsize=figsize).clf()
            plt.loglog(freqs, harm_preds_temp, lw=1, label='')
            plt.title('Fundamental Frequency Prediction')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Power (dB)')
            plt.grid(True)
            plt.tight_layout()
            harm_fund_freq_preds.append(get_graph())
    return harm_fund_freq_preds

def get_PS(lib_list):
    ps_chart_list = []
    if lib_list:
        for lib_entry in lib_list:
            ps_fft_data = librosa.stft(lib_entry[1])
            ps_fft_db_data = librosa.amplitude_to_db(abs(ps_fft_data), ref=np.max)
            plt.figure(1, figsize=figsize).clf()
            librosa.display.specshow(
                ps_fft_db_data,
                sr=lib_entry[0],
                x_axis='time',
                y_axis='log',
            )
            plt.colorbar(format='%+2.f dB')
            plt.title('Power Spectrum')
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
            plt.tight_layout()
            ps_chart_list.append(get_graph())
    return ps_chart_list

def get_mellin(lib_list):
    mellin_chart_list = []
    if lib_list:
        for lib_entry in lib_list:            
            mel_spec = librosa.feature.melspectrogram(y=lib_entry[1], sr=lib_entry[0])
            mel_spec_dB = librosa.power_to_db(mel_spec, ref=np.max)
            plt.figure(1, figsize=figsize).clf()
            librosa.display.specshow(
                mel_spec_dB,
                sr=lib_entry[0],
                x_axis='time',
                y_axis='log',
            )
            plt.colorbar(format='%+2.f dB')
            plt.title('Mellin Scaled Power Spectrum')
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
            plt.tight_layout()
            mellin_chart_list.append(get_graph())
    return mellin_chart_list

def get_percussive(lib_list):
    perc_chart_list = []
    if lib_list:
        for lib_entry in lib_list:
            spec_fft_data = librosa.stft(lib_entry[1])
            harm, perc = librosa.decompose.hpss(spec_fft_data)
            perc_db_data = librosa.amplitude_to_db(np.abs(perc), ref=np.max(np.abs(spec_fft_data)))
            plt.figure(1, figsize=figsize).clf()
            librosa.display.specshow(
                perc_db_data,
                sr=lib_entry[0],
                x_axis='time',
                y_axis='log',
            )
            plt.colorbar(format='%+2.f dB')
            plt.title('Percussive Components')
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
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
            plt.figure(1, figsize=figsize).clf()
            librosa.display.specshow(
                harm_db_data,
                sr=lib_entry[0],
                x_axis='time',
                y_axis='log',
            )
            plt.colorbar(format='%+2.f dB')
            plt.title('Harmonic Components')
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
            plt.tight_layout()
            harm_chart_list.append(get_graph())
    return harm_chart_list