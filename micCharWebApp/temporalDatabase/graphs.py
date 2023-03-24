import sys
from matplotlib import pyplot as plt
import numpy as np
import librosa
import librosa.display
from micCharacterization.graphic_interfacing import get_graph
from acoustics.cepstrum import complex_cepstrum

fig_size = (6, 4.5)
fig_size_xl = (12, 3)

def get_signal(sig, name, mic_Data_Record):
    sr = sig.fs
    plt.figure(2, figsize=fig_size_xl).clf()
    librosa.display.waveshow(sig[0:int(sr/10)], sr=sr, max_points=sys.maxsize, label='Signal', lw=0.5, alpha=0.75)
    ampl_env = sig.amplitude_envelope()[0:int(sr/10):1]
    t = np.arange(0, 1/10, 1/sr)
    plt.plot(t, ampl_env, 'r', label='Envelope', linestyle='dashed', lw=0.25, alpha=0.75)
    plt.plot(t, -ampl_env, 'r', linestyle='dashed', lw=0.25, alpha=0.75)
    plt.title(name + ' Time Signal & Hilbert Envelope (1st tenth of a second)')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (V)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return get_graph('Temporal Graphs', 'signal_Graph', mic_Data_Record)

def get_cepstrum(sig, name, mic_Data_Record):
    sr = sig.fs
    plt.figure(2, figsize=fig_size_xl).clf()
    t = np.arange(0, 1/10, 1/sr)
    ceps, _ = complex_cepstrum(sig)
    ceps = ceps[0:int(sr/10)]
    plt.plot(t, ceps, lw=0.75, alpha=0.75)
    plt.title(name + ' Cepstrum (1st tenth of a second)')
    plt.xlabel('Time (s)')
    plt.grid(True)
    plt.tight_layout()
    return get_graph('Temporal Graphs', 'cepstrum_Graph', mic_Data_Record)

def get_inst_phase(sig, name, mic_Data_Record):
    sr = sig.fs
    plt.figure(2, figsize=fig_size_xl).clf()
    t = np.arange(0, 1/10, 1/sr)
    inst_phase = sig.instantaneous_phase()[0:int(sr/10)]
    plt.plot(t, inst_phase, lw=1, alpha=0.5)
    plt.title(name + ' Hilbert Phase (1st tenth of a second)')
    plt.xlabel('Time (s)')
    plt.ylabel('Phase (rad)')
    plt.grid(True)
    plt.tight_layout()
    return get_graph('Temporal Graphs', 'hilbert_Phase_Graph', mic_Data_Record)

def get_onset_strength(lib_list, name, mic_Data_Record):
    onset_strength = librosa.onset.onset_strength(y=lib_list[1], sr=lib_list[0])
    times = librosa.times_like(onset_strength, sr=lib_list[0])
    plt.figure(2, figsize=fig_size_xl).clf()
    plt.plot(times, onset_strength/onset_strength.max(), label='Onset Strength', lw=0.5, alpha=0.75)
    plt.title(name + ' Onset Strength')
    plt.xlabel('Time (s)')
    plt.ylabel('Normalized Strength')
    plt.grid(True)
    plt.tight_layout()
    return get_graph('Temporal Graphs', 'onset_Strength_Graph', mic_Data_Record)

def get_lag_autocorrelation(lib_list, name, mic_Data_Record):
    onset_strength = librosa.onset.onset_strength(y=lib_list[1], sr=lib_list[0])
    tempogram = librosa.feature.tempogram(onset_envelope=onset_strength, sr=lib_list[0])
    ac_global = librosa.autocorrelate(onset_strength, max_size=tempogram.shape[0])
    ac_global = librosa.util.normalize(ac_global)
    lag_seconds_local = np.linspace(0, len(lib_list[1])/lib_list[0], num=tempogram.shape[0])
    lag_seconds_global = np.linspace(0, len(lib_list[1])/lib_list[0], num=len(ac_global))
    plt.figure(1, figsize=fig_size).clf()
    plt.plot(lag_seconds_local, np.mean(tempogram, axis=1), label='Mean Local Autocorrelation', alpha=0.75)
    plt.plot(lag_seconds_global, ac_global, '--', alpha=0.5, label='Global Autocorrelation')
    plt.title(name + '\nAutocorrelation')
    plt.legend(loc='lower left')
    plt.xlabel('Lag (s)')
    plt.ylabel('Correlation Coefficient')
    plt.grid(True)
    plt.tight_layout()
    return get_graph('Temporal Graphs', 'lag_Autocorrelation_Graph', mic_Data_Record)

def get_bpm_autocorrelation(lib_list, name, mic_Data_Record):
    onset_strength = librosa.onset.onset_strength(y=lib_list[1], sr=lib_list[0])
    tempogram = librosa.feature.tempogram(onset_envelope=onset_strength, sr=lib_list[0])
    ac_global = librosa.autocorrelate(onset_strength, max_size=tempogram.shape[0])
    ac_global = librosa.util.normalize(ac_global)
    freqs_local = librosa.tempo_frequencies(tempogram.shape[0], sr=lib_list[0])
    freqs_global = librosa.tempo_frequencies(len(ac_global), sr=lib_list[0])
    tempo = librosa.beat.tempo(onset_envelope=onset_strength, sr=lib_list[0])[0]
    plt.figure(1, figsize=fig_size).clf()
    plt.semilogx(freqs_local[1:], np.mean(tempogram[1:], axis=1), label='Mean Local Autocorrelation', base=2, alpha=0.75)
    plt.semilogx(freqs_global[1:], ac_global[1:], '--', alpha=0.5, label='Global Autocorrelation', base=2)
    plt.axvline(tempo, color='black', linestyle='--', alpha=0.75, label='Estimated Tempo = {:g}'.format(tempo))
    plt.title(name + '\nAutocorrelation')
    plt.legend(frameon=True)
    plt.xlabel('BPM')
    plt.ylabel('Correlation Coefficient')
    plt.grid(True)
    plt.tight_layout()
    return get_graph('Temporal Graphs', 'BPM_Autocorrelation_Graph', mic_Data_Record)

def get_autocorr_tempogram(lib_list, name, mic_Data_Record):
    tempogram = librosa.feature.tempogram(y=lib_list[1], sr=lib_list[0])
    tempo = librosa.beat.tempo(y=lib_list[1], sr=lib_list[0])[0]
    plt.figure(1, figsize=fig_size).clf()
    temp = librosa.display.specshow(tempogram, sr=lib_list[0], cmap='turbo', x_axis='time', y_axis='tempo')
    plt.colorbar(temp)
    plt.axhline(tempo, color='w', linestyle='--', alpha=1, label='Estimated tempo = {:g}'.format(tempo))
    plt.legend(loc='upper right')
    plt.title(name + '\nAutocorrelation Tempogram')
    plt.xlabel('Time (s)')
    plt.tight_layout()
    return get_graph('Temporal Graphs', 'autocorrelation_Tempogram', mic_Data_Record)

def get_fourier_tempogram(lib_list, name, mic_Data_Record):
    tempogram = librosa.feature.fourier_tempogram(y=lib_list[1], sr=lib_list[0])
    this_sum = np.sum(lib_list[1][~(lib_list[1] == 0)])
    tempogram[~np.isfinite(tempogram)] = 0.0
    tempo = librosa.beat.tempo(y=lib_list[1], sr=lib_list[0])[0]
    plt.figure(1, figsize=fig_size).clf()
    temp = librosa.display.specshow(np.abs(tempogram)/np.abs(tempogram).max(), sr=lib_list[0], cmap='turbo', x_axis='time', y_axis='fourier_tempo')
    plt.colorbar(temp)
    plt.axhline(tempo, color='w', linestyle='--', alpha=1, label='Estimated tempo = {:g}'.format(tempo))
    plt.legend(loc='upper right')
    plt.title(name + '\nFourier Tempogram')
    plt.xlabel('Time (s)')
    plt.tight_layout()
    return get_graph('Temporal Graphs', 'fourier_Tempogram', mic_Data_Record)