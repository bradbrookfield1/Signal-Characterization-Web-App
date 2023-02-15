import librosa
from acoustics import Signal
from matplotlib import pyplot as plt

def load_file(wav_name):
    if not wav_name:
        return None
    else:
        sig = Signal.from_wav(wav_name)
        lib_time_data, lib_time_samplerate = librosa.load(wav_name, sr=96000)
        lib_snr_data, lib_snr_samplerate = librosa.load(wav_name, sr=2000)
        lib_list = [lib_time_samplerate, lib_time_data]
        lib_snr_list = [lib_snr_samplerate, lib_snr_data]
        return lib_list, sig, lib_snr_list

def charts_preprocess(file_list=None):
    plt.switch_backend('AGG')
    # file_list --> [noisy_sig, sig, noise, ref_noisy_sig, ref_sig, ref_noise]
    
    # (lib, sig)
    noisy_sig_list = load_file(file_list[0])       # Noisy signal
    sig_list = load_file(file_list[1])             # Measured signal
    noise_list = load_file(file_list[2])           # Pure noise
    true_sig = load_file(file_list[3])             # True signal
    
    ref_noisy_sig_list = load_file(file_list[4])   # Reference noisy signal
    ref_sig_list = load_file(file_list[5])         # Reference signal
    ref_noise_list = load_file(file_list[6])       # Reference noise
    norm_noisy_sig, norm_sig, norm_noise = normalize_signals(noisy_sig_list, sig_list, noise_list, ref_noisy_sig_list, ref_sig_list, ref_noise_list)    
    return norm_noisy_sig, norm_sig, norm_noise, true_sig

def normalize_signals(noisy_sig_list=None, sig_list=None, noise_list=None, ref_noisy_sig_list=None, ref_sig_list=None, ref_noise_list=None):
    ret = []
    ret.append(noisy_sig_list) if ref_noisy_sig_list == None else ret.append(ref_noisy_sig_list)
    ret.append(sig_list) if ref_sig_list == None else ret.append(ref_sig_list)
    ret.append(noise_list) if ref_noise_list == None else ret.append(ref_noise_list)
    return ret