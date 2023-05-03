import math
from matplotlib import pyplot as plt
from scipy import signal
import numpy as np
import pandas as pd
import librosa
import librosa.display
from micCharacterization.graphic_interfacing import get_graph
from micCharacterization.calculations import fft_vectorized

fig_size = (6, 4.5)

def get_PSD(lib_list, name, mic_Data_Record):
    avg_freq, avg_data = signal.welch(x=lib_list[1], fs=lib_list[0], average='mean')
    avg_data_pd = pd.Series(avg_data).rolling(13, center=True).mean().to_numpy()
    plt.figure(1, figsize=fig_size).clf()
    plt.semilogy(avg_freq, avg_data, label='Raw PSD', lw=1, alpha=0.75)
    plt.semilogy(avg_freq, avg_data_pd, label='Rolled', lw=1, alpha=0.75)
    plt.title(name + '\nPower Spectral Density Estimate')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel(r'Power Spectral Density $\left(\frac{V^{2}}{Hz}\right)$')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return get_graph('Spectral Graphs', 'average_PSD_Graph', mic_Data_Record)

def get_phase_spectrum(sig, name, mic_Data_Record):
    plt.figure(1, figsize=fig_size).clf()
    freq, sig = sig.phase_spectrum()
    plt.plot(freq, sig, alpha=0.75)
    plt.title(name + '\nPhase Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase (rad)')
    plt.grid(True)
    plt.tight_layout()
    return get_graph('Spectral Graphs', 'phase_Spectrum_Graph', mic_Data_Record)

def get_noise_PSD(lib_list, name, mic_Data_Record):
    avg_freq, avg_data = signal.welch(x=lib_list[1], fs=lib_list[0], average='mean')
    avg_data_pd = pd.Series(avg_data).rolling(13, center=True).mean().to_numpy()
    plt.figure(1, figsize=fig_size).clf()
    plt.semilogy(avg_freq, avg_data, label='Raw PSD', lw=1, alpha=0.75)
    plt.semilogy(avg_freq, avg_data_pd, label='Rolled', lw=1, alpha=0.75)
    plt.title(name + '\nPower Spectral Density Estimate')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel(r'Power Spectral Density $\left(\frac{V^{2}}{Hz}\right)$')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return get_graph('Spectral Graphs', 'noise_PSD_Graph', mic_Data_Record)

def get_overlapping_PSD(noisy_sig, noise, name, mic_Data_Record):
    noisy_sig_freq, noisy_sig_data = signal.welch(x=noisy_sig[1], fs=noisy_sig[0], average='mean')
    noisy_sig_data_pd = pd.Series(noisy_sig_data).rolling(13, center=True).mean().to_numpy()
    noise_freq, noise_data = signal.welch(x=noise[1], fs=noise[0], average='mean')
    noise_data_pd = pd.Series(noise_data).rolling(13, center=True).mean().to_numpy()
    plt.figure(1, figsize=fig_size).clf()
    plt.semilogy(noisy_sig_freq, noisy_sig_data, label='S + N PSD', lw=1, alpha=0.75)
    plt.semilogy(noisy_sig_freq, noisy_sig_data_pd, label='S + N Rolled', lw=1, alpha=0.75)
    plt.semilogy(noise_freq, noise_data, label='N PSD', lw=1, alpha=0.75)
    plt.semilogy(noise_freq, noise_data_pd, label='N Rolled', lw=1, alpha=0.75)
    plt.title(name + '\nPower Spectral Density Estimate')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel(r'Power Spectral Density $\left(\frac{V^{2}}{Hz}\right)$')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return get_graph('Spectral Graphs', 'overlapping_PSD_Graph', mic_Data_Record)

def get_spectrogram(lib_list, name, mic_Data_Record):
    ps_fft_data = librosa.stft(lib_list[1])
    ps_fft_db_data = librosa.amplitude_to_db(np.abs(ps_fft_data), ref=np.max)
    # ps_fft_db_data[~np.isfinite(ps_fft_db_data)] = -100
    plt.figure(1, figsize=fig_size).clf()
    librosa.display.specshow(
        ps_fft_db_data,
        sr=lib_list[0],
        cmap='turbo',
        x_axis='time',
        y_axis='log',
    )
    plt.colorbar(format='%+2.f dB')
    plt.title(name + '\nSpectrogram')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.tight_layout()
    return get_graph('Spectral Graphs', 'spectrogram', mic_Data_Record)

def get_mellin(lib_list, name, mic_Data_Record):
    mel_spec = librosa.feature.melspectrogram(y=lib_list[1], sr=lib_list[0])
    mel_spec_dB = librosa.power_to_db(mel_spec, ref=np.max)
    # mel_spec_dB[~np.isfinite(mel_spec_dB)] = -100
    plt.figure(1, figsize=fig_size).clf()
    librosa.display.specshow(
        mel_spec_dB,
        sr=lib_list[0],
        cmap='turbo',
        x_axis='time',
        y_axis='log',
    )
    plt.colorbar(format='%+2.f dB')
    plt.title(name + '\nMellin Scaled Spectrogram')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.tight_layout()
    return get_graph('Spectral Graphs', 'mellin_Spectrogram', mic_Data_Record)

def get_percussive(lib_list, name, mic_Data_Record):
    spec_fft_data = librosa.stft(lib_list[1])
    harm, perc = librosa.decompose.hpss(spec_fft_data)
    # perc_play = librosa.istft(perc)
    perc_db_data = librosa.amplitude_to_db(np.abs(perc), ref=np.max(np.abs(spec_fft_data)))
    # perc_db_data[~np.isfinite(perc_db_data)] = -100
    plt.figure(1, figsize=fig_size).clf()
    librosa.display.specshow(
        perc_db_data,
        sr=lib_list[0],
        cmap='turbo',
        x_axis='time',
        y_axis='log',
    )
    plt.colorbar(format='%+2.f dB')
    plt.title(name + '\nPercussive Components')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.tight_layout()
    return get_graph('Spectral Graphs', 'percussive_Spectrogram', mic_Data_Record)

def get_harmonic(lib_list, name, mic_Data_Record):
    spec_fft_data = librosa.stft(lib_list[1])
    harm, perc = librosa.decompose.hpss(spec_fft_data)
    harm_db_data = librosa.amplitude_to_db(np.abs(harm), ref=np.max(np.abs(spec_fft_data)))
    # harm_db_data[~np.isfinite(harm_db_data)] = -100
    plt.figure(1, figsize=fig_size).clf()
    librosa.display.specshow(
        harm_db_data,
        sr=lib_list[0],
        cmap='turbo',
        x_axis='time',
        y_axis='log',
    )
    plt.colorbar(format='%+2.f dB')
    plt.title(name + '\nHarmonic Components')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.tight_layout()
    return get_graph('Spectral Graphs', 'harmonic_Spectrogram', mic_Data_Record)

def get_harmonic_prediction(lib_list, num_harmonics, name, mic_Data_Record):
    tm = len(lib_list[1])/lib_list[0]
    pow_of_2 = np.int64(np.floor(np.log2(len(lib_list[1]))))
    lib_time_data = signal.resample(lib_list[1], np.power(2, pow_of_2))
    new_sr = len(lib_time_data)/tm
    for r in range(1, num_harmonics + 1):
        if r == 1:
            harm_preds_temp = np.array(fft_vectorized(lib_time_data, r))
        else:
            harm_preds_temp = np.vstack((harm_preds_temp, fft_vectorized(lib_time_data, r)))
    harm_preds_temp = np.abs(harm_preds_temp)**(-1)
    harm_preds_temp = (np.sum(harm_preds_temp, axis=0)/num_harmonics)**(-1)
    harm_preds_temp = librosa.amplitude_to_db(harm_preds_temp)
    freqs = librosa.fft_frequencies(sr=new_sr, n_fft=len(lib_time_data)*2)[1:]
    plt.figure(1, figsize=fig_size).clf()
    plt.plot(freqs, harm_preds_temp, label='', lw=1, alpha=0.75)
    plt.title(name + '\nFundamental Frequency Prediction')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power (dB)')
    plt.grid(True)
    plt.tight_layout()
    return get_graph('Spectral Graphs', 'harmonic_Prediction_Graph', mic_Data_Record)