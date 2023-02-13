import base64, os, librosa
from io import BytesIO
from matplotlib import pyplot as plt
from acoustics import Signal

def file_path_to_img(file_path):
    if file_path == None:
        return None
    img = open(file_path, 'rb').read()
    img = base64.b64encode(img)
    return img.decode('utf-8')

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
        
        # pos = wav_name.find('+')
        # neg = wav_name.find('-')
        # dB = wav_name.find('dB')
        # if dB == -1:
        #     lib_list = [lib_time_samplerate, lib_time_data]
        #     return lib_list, sig
        
        # idx = dB
        # while not wav_name[idx] == '_':
        #     idx = idx - 1
        # if wav_name[idx + 1] == '-':
        #     ampFactor = float(wav_name[idx + 2:dB:1])
        # else:
        #     ampFactor = -float(wav_name[idx + 1:dB:1])

        # sig.gain(ampFactor)
        
        # lib = librosa.amplitude_to_db(librosa.stft(lib_time_data))
        # lib = lib + ampFactor
        # lib = librosa.istft(librosa.db_to_amplitude(lib))
        
        # # ampFactor = 10**(ampFactor/20)
        # # for data in lib_time_data:
        # #     data = data*ampFactor
        
        # lib_list = [lib_time_samplerate, lib]
        # return lib_list, sig

def normalize_signals(noisy_sig_list=None, sig_list=None, noise_list=None, ref_noisy_sig_list=None, ref_sig_list=None, ref_noise_list=None):
    ret = []
    ret.append(noisy_sig_list) if ref_noisy_sig_list == None else ret.append(ref_noisy_sig_list)
    ret.append(sig_list) if ref_sig_list == None else ret.append(ref_sig_list)
    ret.append(noise_list) if ref_noise_list == None else ret.append(ref_noise_list)
    return ret

def get_graph(temp_spec, attr, mic_Data_Record):
    full_name = 'Uploads/' + temp_spec + '/' + attr + '/' + attr + '_' + str(mic_Data_Record.pk) + '.png'
    if os.path.exists(full_name):
        os.remove(full_name)
    plt.savefig(full_name)
    return full_name

def get_abs_coeff_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    buffer.close()
    return graph.decode('utf-8')

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