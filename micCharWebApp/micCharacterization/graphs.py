import sys
from matplotlib import pyplot as plt
from scipy import signal
import numpy as np
import librosa
import librosa.display
from .graphic_interfacing import get_graph

width = 3.75
height = 2.8125
figsize = (width, height)
figsize_xl = (width*3, height)

def get_signal(lib_list, dur_list):
    sig_chart_list = []
    if lib_list:
        for idx, lib_entry in enumerate(lib_list):
            plt.figure(2, figsize=figsize_xl).clf()
            librosa.display.waveshow(lib_entry[1][0:int(96000/10)], sr=lib_entry[0], max_points=sys.maxsize, offset=dur_list[idx][0])
            plt.title('Time Domain Original Signal (first tenth of a second)')
            plt.xlabel('Time (seconds)')
            plt.ylabel('Amplitude')
            plt.tight_layout()
            sig_chart_list.append(get_graph())
    return sig_chart_list

def get_lag_autocorrelation(lib_list):
    lag_autocorr_list = []
    if lib_list:
        for lib_entry in lib_list:
            onset_strength = librosa.onset.onset_strength(y=lib_entry[1], sr=lib_entry[0])
            tempogram = librosa.feature.tempogram(onset_envelope=onset_strength, sr=lib_entry[0])
            ac_global = librosa.autocorrelate(onset_strength, max_size=tempogram.shape[0])
            ac_global = librosa.util.normalize(ac_global)
            lag_seconds = np.linspace(0, len(lib_entry[1]) / lib_entry[0], num=tempogram.shape[0])
            plt.figure(1, figsize=figsize).clf()
            plt.plot(lag_seconds, np.mean(tempogram, axis=1), label='Mean Local Autocorrelation')
            plt.plot(lag_seconds, ac_global, '--', alpha=0.75, label='Global Autocorrelation')
            plt.title('Autocorrelation')
            plt.legend(loc='lower left')
            plt.xlabel('Lag (seconds)')
            plt.grid(True)
            plt.tight_layout()
            lag_autocorr_list.append(get_graph())
    return lag_autocorr_list

def get_bpm_autocorrelation(lib_list):
    bpm_autocorr_list = []
    if lib_list:
        for lib_entry in lib_list:
            onset_strength = librosa.onset.onset_strength(y=lib_entry[1], sr=lib_entry[0])
            tempogram = librosa.feature.tempogram(onset_envelope=onset_strength, sr=lib_entry[0])
            ac_global = librosa.autocorrelate(onset_strength, max_size=tempogram.shape[0])
            ac_global = librosa.util.normalize(ac_global)
            freqs = librosa.tempo_frequencies(tempogram.shape[0], sr=lib_entry[0])
            tempo = librosa.beat.tempo(onset_envelope=onset_strength, sr=lib_entry[0])[0]
            plt.figure(1, figsize=figsize).clf()
            plt.semilogx(freqs[1:], np.mean(tempogram[1:], axis=1), label='Mean Local Autocorrelation', base=2)
            plt.semilogx(freqs[1:], ac_global[1:], '--', alpha=0.75, label='Global Autocorrelation', base=2)
            plt.axvline(tempo, color='black', linestyle='--', alpha=.8, label='Estimated Tempo = {:g}'.format(tempo))
            plt.title('Autocorrelation')
            plt.legend(frameon=True)
            plt.xlabel('BPM')
            plt.grid(True)
            plt.tight_layout()
            bpm_autocorr_list.append(get_graph())
    return bpm_autocorr_list

def get_onset_strength(lib_list):
    onset_strength_list = []
    if lib_list:
        for lib_entry in lib_list:
            onset_strength = librosa.onset.onset_strength(y=lib_entry[1], sr=lib_entry[0])
            times = librosa.times_like(onset_strength, sr=lib_entry[0])
            plt.figure(2, figsize=figsize_xl).clf()
            plt.plot(times, onset_strength/onset_strength.max(), label='Onset strength')
            plt.title('Onset Strength')
            plt.xlabel('Time (seconds)')
            plt.tight_layout()
            onset_strength_list.append(get_graph())
    return onset_strength_list

def get_fourier_tempogram(lib_list):
    tempo_chart_list = []
    if lib_list:
        for lib_entry in lib_list:
            tempogram = librosa.feature.fourier_tempogram(y=lib_entry[1], sr=lib_entry[0])
            tempo = librosa.beat.tempo(y=lib_entry[1], sr=lib_entry[0])[0]
            plt.figure(1, figsize=figsize).clf()
            temp = librosa.display.specshow(np.abs(tempogram)/np.abs(tempogram).max(), sr=lib_entry[0], x_axis='time', y_axis='fourier_tempo', cmap='magma')
            plt.colorbar(temp)
            plt.axhline(tempo, color='w', linestyle='--', alpha=1, label='Estimated tempo = {:g}'.format(tempo))
            plt.legend(loc='upper right')
            plt.title('Fourier Tempogram')
            plt.xlabel('Time (seconds)')
            plt.tight_layout()
            tempo_chart_list.append(get_graph())
    return tempo_chart_list

def get_autocorr_tempogram(lib_list):
    tempo_chart_list = []
    if lib_list:
        for lib_entry in lib_list:
            tempogram = librosa.feature.tempogram(y=lib_entry[1], sr=lib_entry[0])
            tempo = librosa.beat.tempo(y=lib_entry[1], sr=lib_entry[0])[0]
            plt.figure(1, figsize=figsize).clf()
            temp = librosa.display.specshow(tempogram, sr=lib_entry[0], x_axis='time', y_axis='tempo', cmap='magma')
            plt.colorbar(temp)
            plt.axhline(tempo, color='w', linestyle='--', alpha=1, label='Estimated tempo = {:g}'.format(tempo))
            plt.legend(loc='upper right')
            plt.title('Autocorrelation Tempogram')
            plt.xlabel('Time (seconds)')
            plt.tight_layout()
            tempo_chart_list.append(get_graph())
    return tempo_chart_list

def get_avg_power(lib_list):    
    avg_chart_list = []
    if lib_list:
        for lib_entry in lib_list:            
            avg_freq, avg_data = signal.welch(x=lib_entry[1], fs=lib_entry[0])
            plt.figure(1, figsize=figsize).clf()
            plt.loglog(avg_freq, avg_data, lw=1, label='')
            plt.title('Average Power')
            plt.xlabel('Frequency')
            plt.ylabel('Voltage^2')
            plt.grid(True)
            plt.tight_layout()
            avg_chart_list.append(get_graph())
    return avg_chart_list

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
            plt.tight_layout()
            harm_chart_list.append(get_graph())
    return harm_chart_list

def get_harmonic_transform(lib_list):
    return