import librosa
import numpy as np
from acoustics import Signal
from matplotlib import pyplot as plt

def load_file(wav_name):
    if not wav_name:
        return None
    else:
        sig = Signal.from_wav(wav_name)
        sig = sig if not (len(sig) == 2 or len(sig) == 4) else sig[0]
        # lib_time_data, lib_time_samplerate = librosa.load(wav_name, sr=48000, mono=False)
        # lib_snr_data, lib_snr_samplerate = librosa.load(wav_name, sr=2000, mono=False)
        lib_time_data, lib_time_samplerate = librosa.load(wav_name, sr=48000)
        lib_snr_data, lib_snr_samplerate = librosa.load(wav_name, sr=2000)
        
        # print(sig.shape)
        # print(lib_time_data.shape)
        # print()
        # print(sig[0])
        # print(lib_time_data[0])
        # print()
        # print(sig[1])
        # print(lib_time_data[1])
        # print()
        # print(sig[2])
        # print(lib_time_data[2])
        # print()
        # print(sig[3])
        # print(lib_time_data[3])
        # print()
        
        # lib_time_data = np.float64(librosa.mu_compress(lib_time_data))
        
        # lib_snr_data = np.float64(librosa.mu_compress(lib_snr_data))

        lib_list = [lib_time_samplerate, lib_time_data]
        lib_snr_list = [lib_snr_samplerate, lib_snr_data]
        return lib_list, sig, lib_snr_list

def charts_preprocess(file_list=None):
    plt.switch_backend('AGG')
    # file_list --> [noisy_sig, sig, noise, true_sig]
    
    # (lib, sig)
    noisy_sig_list = load_file(file_list[0])       # Noisy signal
    sig_list = load_file(file_list[1])             # Measured signal
    noise_list = load_file(file_list[2])           # Pure noise
    true_sig = load_file(file_list[3])             # True signal
    return noisy_sig_list, sig_list, noise_list, true_sig