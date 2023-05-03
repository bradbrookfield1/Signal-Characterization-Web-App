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
        # sig = sig if len(sig) == 2 or len(sig) == 4 else [sig]
        sig = sig if not (len(sig) == 2 or len(sig) == 4) else sig[0]
        
        # lib_time_data, lib_time_samplerate = librosa.load(wav_name, sr=sr, mono=False)
        # lib_snr_data, lib_snr_samplerate = librosa.load(wav_name, sr=8000, mono=False)
        lib_time_data, lib_time_samplerate = librosa.load(wav_name, sr=sr)
        lib_snr_data, lib_snr_samplerate = librosa.load(wav_name, sr=8000)

        lib_list = [lib_time_samplerate, lib_time_data]
        lib_snr_list = [lib_snr_samplerate, lib_snr_data]
        return lib_list, sig, lib_snr_list

def apply_norm_to_lib(lib):
    # return np.int16((lib/np.max(np.abs(lib)))*32767)
    return (lib - np.mean(lib))/np.std(lib)

def apply_norm_to_Signal(sig):
    return Signal((sig - np.mean(sig))/np.std(sig), fs=sig.fs)

def apply_stat_norm_everywhere(noisy_sig, noise):
    ns_mean = [np.mean(noisy_sig[0][1]), np.mean(noisy_sig[1]), np.mean(noisy_sig[2][1])]
    ns_std = [np.std(noisy_sig[0][1]), np.std(noisy_sig[1]), np.std(noisy_sig[2][1])]
    n_mean = [np.mean(noise[0][1]), np.mean(noise[1]), np.mean(noise[2][1])]
    n_std = [np.std(noise[0][1]), np.std(noise[1]), np.std(noise[2][1])]
    mean_diff = [ns_mean[0] - n_mean[0], ns_mean[1] - n_mean[1], ns_mean[2] - n_mean[2]]
    
    norm_lib_n = (noise[0][1] - n_mean[0])/n_std[0]
    norm_sig_n = Signal((noise[1] - n_mean[1])/n_std[1], fs=noise[1].fs)
    norm_snr_n = (noise[2][1] - n_mean[2])/n_std[2]
    new_n = [[noise[0][0], norm_lib_n], norm_sig_n, [noise[2][0], norm_snr_n]]
    
    norm_lib_ns = (noisy_sig[0][1] - ns_mean[0])/ns_std[0] + mean_diff[0]
    norm_sig_ns = Signal((noisy_sig[1] - ns_mean[1])/ns_std[1] + mean_diff[1], fs=noisy_sig[1].fs)
    norm_snr_ns = (noisy_sig[0][1] - ns_mean[2])/ns_std[2] + mean_diff[2]
    new_ns = [[noisy_sig[0][0], norm_lib_ns], norm_sig_ns, [noisy_sig[2][0], norm_snr_ns]]
    return new_ns, new_n

def apply_norm_everywhere(sig_struct):
    return [[sig_struct[0][0], apply_norm_to_lib(sig_struct[0][1])], apply_norm_to_Signal(sig_struct[1]), [sig_struct[2][0], apply_norm_to_lib(sig_struct[2][1])]]

def apply_bp_to_lib(lib, low_high, order):
    return [lib[0], butter_bandpass_filter(lib[1], low_high, lib[0], order)]

def apply_bp_to_Signal(sig, low_high, order, snr=False):
    return Signal(butter_bandpass_filter(sig, low_high, sig.fs, order), fs=sig.fs)

def apply_bp_everywhere(sig_struct, low_high, order=4, snr=False):
    term1 = apply_bp_to_lib(sig_struct[0], low_high, order)
    term2 = apply_bp_to_Signal(sig_struct[1], low_high, order, snr)
    term3 = apply_bp_to_lib(sig_struct[2], low_high, order)
    return [term1, term2, term3]

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