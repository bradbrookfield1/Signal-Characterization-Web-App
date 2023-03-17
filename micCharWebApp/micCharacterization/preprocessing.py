import librosa
import numpy as np
from acoustics import Signal
from matplotlib import pyplot as plt

def load_file(wav_name):
    if not wav_name:
        return None
    else:
        sig = Signal.from_wav(wav_name)
        if len(sig) == 4:
            sig1 = sig[0]
            sig2 = sig[1]
            sig3 = sig[2]
            sig4 = sig[3]
        else:
            sig1 = sig
        lib_time_data, lib_time_samplerate = librosa.load(wav_name, sr=48000)
        lib_snr_data, lib_snr_samplerate = librosa.load(wav_name, sr=2000)
        
        # lib_time_data = np.float64(librosa.mu_compress(lib_time_data))
        
        # lib_snr_data = np.float64(librosa.mu_compress(lib_snr_data))

        lib_list = [lib_time_samplerate, lib_time_data]
        lib_snr_list = [lib_snr_samplerate, lib_snr_data]
        return lib_list, sig1, lib_snr_list

def charts_preprocess(file_list=None):
    plt.switch_backend('AGG')
    # file_list --> [noisy_sig, sig, noise, ref_noisy_sig, ref_sig, ref_noise]
    
    # (lib, sig)
    noisy_sig_list = load_file(file_list[0])       # Noisy signal
    sig_list = load_file(file_list[1])             # Measured signal
    noise_list = load_file(file_list[2])           # Pure noise
    true_sig = load_file(file_list[3])             # True signal
    return noisy_sig_list, sig_list, noise_list, true_sig