import librosa, math
import numpy as np
from scipy.signal import butter, filtfilt
from acoustics import Signal
from matplotlib import pyplot as plt

def load_file(wav_name):
    if not wav_name:
        return None
    else:
        sig = Signal.from_wav(wav_name, normalize=False)
        sr = sig.fs
        sig = sig if not (len(sig) == 2 or len(sig) == 4) else sig[0]
        
        # lib_time_data, lib_time_samplerate = librosa.load(wav_name, sr=48000, mono=False)
        # lib_snr_data, lib_snr_samplerate = librosa.load(wav_name, sr=2000, mono=False)
        lib_time_data, lib_time_samplerate = librosa.load(wav_name, sr=sr)
        lib_snr_data, lib_snr_samplerate = librosa.load(wav_name, sr=2000)

        lib_list = [lib_time_samplerate, lib_time_data]
        lib_snr_list = [lib_snr_samplerate, lib_snr_data]
        return lib_list, sig, lib_snr_list

def apply_norm_to_lib(lib):
    return [lib[0], np.int16((lib[1]/np.max(np.abs(lib[1])))*32767)]

def apply_norm_to_Signal(sig):
    sr = sig.fs
    return Signal(apply_norm_to_lib([sr, np.asarray(sig)]), fs=sr)

def apply_norm_everywhere(sig_struct):
    return [apply_norm_to_lib(sig_struct[0]), apply_norm_to_Signal(sig_struct[1]), apply_norm_to_lib(sig_struct[2])]

def apply_bp_to_lib(lib, low_high, order):
    return [lib[0], butter_bandpass_filter(lib[1], low_high, lib[0], order)]

def apply_bp_to_Signal(sig, low_high, order, snr=False):
    sr = sig.fs
    if snr:
        return Signal(butter_bandpass_filter(sig, low_high, sr, order), fs=sr)
    return Signal(butter_bandpass_filter(sig[1], low_high, sr, order), fs=sr)

def apply_bp_everywhere(sig_struct, low_high, order=4, snr=False):
    return [apply_bp_to_lib(sig_struct[0], low_high, order), apply_bp_to_Signal(sig_struct[1], low_high, order, snr), apply_bp_to_lib(sig_struct[2], low_high, order)]

def charts_preprocess(file_list=None):
    plt.switch_backend('AGG')
    # file_list --> [noisy_sig, sig, noise, true_sig]
    
    # (lib, sig)
    noisy_sig_list = load_file(file_list[0])       # Noisy signal
    sig_list = load_file(file_list[1])             # Measured signal
    noise_list = load_file(file_list[2])           # Pure noise
    true_sig = load_file(file_list[3])             # True signal
    return noisy_sig_list, sig_list, noise_list, true_sig

def butter_bandpass(low_high, fs, order):
    nyq = 0.5 * fs
    low = low_high[0] / nyq
    high = low_high[1] / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, low_high, fs, order):
    b, a = butter_bandpass(low_high, fs, order)
    y = filtfilt(b, a, data)
    # y[~np.isfinite(y)] = 0.0
    y = y.astype(np.float32)
    return y

def assign_hpss_arrays(context, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record):
    context['noisy_Signal_Harmonics'] = mic_Data_Record.noisy_Signal_Harmonics if norm_noisy_sig else None
    context['noisy_Signal_Percussives'] = mic_Data_Record.noisy_Signal_Percussives if norm_noisy_sig else None
    context['measured_Signal_Harmonics'] = mic_Data_Record.measured_Signal_Harmonics if norm_sig else None
    context['measured_Signal_Percussives'] = mic_Data_Record.measured_Signal_Percussives if norm_sig else None
    context['noise_Harmonics'] = mic_Data_Record.noise_Harmonics if norm_noise else None
    context['noise_Percussives'] = mic_Data_Record.noise_Percussives if norm_noise else None
    context['true_Signal_Harmonics'] = mic_Data_Record.true_Signal_Harmonics if true_sig else None
    context['true_Signal_Percussives'] = mic_Data_Record.true_Signal_Percussives if true_sig else None
    
    ns_harm_name = './Uploads/' + context['noisy_Signal_Harmonics'].name if context['noisy_Signal_Harmonics'] else None
    s_harm_name = './Uploads/' + context['measured_Signal_Harmonics'].name if context['measured_Signal_Harmonics'] else None
    n_harm_name = './Uploads/' + context['noise_Harmonics'].name if context['noise_Harmonics'] else None
    ts_harm_name = './Uploads/' + context['true_Signal_Harmonics'].name if context['true_Signal_Harmonics'] else None
    ns_perc_name = './Uploads/' + context['noisy_Signal_Percussives'].name if context['noisy_Signal_Percussives'] else None
    s_perc_name = './Uploads/' + context['measured_Signal_Percussives'].name if context['measured_Signal_Percussives'] else None
    n_perc_name = './Uploads/' + context['noise_Percussives'].name if context['noise_Percussives'] else None
    ts_perc_name = './Uploads/' + context['true_Signal_Percussives'].name if context['true_Signal_Percussives'] else None
    
    ns_harm, s_harm, n_harm, ts_harm = charts_preprocess([ns_harm_name, s_harm_name, n_harm_name, ts_harm_name])
    ns_perc, s_perc, n_perc, ts_perc = charts_preprocess([ns_perc_name, s_perc_name, n_perc_name, ts_perc_name])
    hpss_array = [ns_harm, ns_perc, s_harm, s_perc, n_harm, n_perc, ts_harm, ts_perc]
    return context, hpss_array