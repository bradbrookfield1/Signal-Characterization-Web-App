import sys
from matplotlib import pyplot as plt
import numpy as np
import librosa
import librosa.display
from .graphic_interfacing import get_graph
from acoustics.cepstrum import complex_cepstrum

width = 3.75
height = 2.8125
figsize = (width, height)
figsize_xl = (width*3, height)

def get_signal(lib_list, dur_list, sig_list):
    sig_chart_list = []
    if lib_list:
        i = range(len(lib_list))
        for idx, lib_entry, sig_entry in zip(i, lib_list, sig_list):
            plt.figure(2, figsize=figsize_xl).clf()
            librosa.display.waveshow(sig_entry[0:int(lib_entry[0]/10)], sr=lib_entry[0], max_points=sys.maxsize, offset=dur_list[idx][0], label='Signal')
            sig = sig_entry.amplitude_envelope()[0:int(lib_entry[0]/10):1]
            t = np.arange(0, 1/10, 1/lib_entry[0])
            plt.plot(t, sig, 'r', label='Envelope')
            plt.plot(t, -sig, 'r')
            plt.title('Time Signal & Hilbert Envelope (1st tenth of a second)')
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude (V)')
            plt.legend()
            plt.tight_layout()
            sig_chart_list.append(get_graph())
    return sig_chart_list

def get_cepstrum(lib_list, sig_list):
    cepstrum_chart_list = []
    if sig_list:
        for lib_entry, sig_entry in zip(lib_list, sig_list):
            plt.figure(2, figsize=figsize_xl).clf()
            t = np.arange(0, 1/10, 1/lib_entry[0])
            sig, _ = complex_cepstrum(sig_entry)
            sig = sig[0:int(lib_entry[0]/10)]
            plt.plot(t, sig)
            plt.title('Cepstrum (1st tenth of a second)')
            plt.xlabel('Time (s)')
            plt.grid(True)
            plt.tight_layout()
            cepstrum_chart_list.append(get_graph())
    return cepstrum_chart_list

def get_inst_phase(lib_list, sig_list):
    hilbert_chart_list = []
    if sig_list:
        for lib_entry, sig_entry in zip(lib_list, sig_list):
            plt.figure(2, figsize=figsize_xl).clf()
            t = np.arange(0, 1/10, 1/lib_entry[0])
            sig = sig_entry.instantaneous_phase()[0:int(lib_entry[0]/10)]
            plt.plot(t, sig)
            plt.title('Hilbert Phase (1st tenth of a second)')
            plt.xlabel('Time (s)')
            plt.ylabel('Phase (rad)')
            plt.grid(True)
            plt.tight_layout()
            hilbert_chart_list.append(get_graph())
    return hilbert_chart_list

def get_onset_strength(lib_list):
    onset_strength_list = []
    if lib_list:
        for lib_entry in lib_list:
            onset_strength = librosa.onset.onset_strength(y=lib_entry[1], sr=lib_entry[0])
            times = librosa.times_like(onset_strength, sr=lib_entry[0])
            plt.figure(2, figsize=figsize_xl).clf()
            plt.plot(times, onset_strength/onset_strength.max(), label='Onset strength')
            plt.title('Onset Strength')
            plt.xlabel('Time (s)')
            plt.ylabel('Normalized Strength')
            plt.tight_layout()
            onset_strength_list.append(get_graph())
    return onset_strength_list

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
            plt.xlabel('Lag (s)')
            plt.ylabel('Correlation Coefficient')
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
            plt.ylabel('Correlation Coefficient')
            plt.grid(True)
            plt.tight_layout()
            bpm_autocorr_list.append(get_graph())
    return bpm_autocorr_list

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
            plt.xlabel('Time (s)')
            plt.tight_layout()
            tempo_chart_list.append(get_graph())
    return tempo_chart_list

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
            plt.xlabel('Time (s)')
            plt.tight_layout()
            tempo_chart_list.append(get_graph())
    return tempo_chart_list