import base64, os, librosa
from matplotlib import pyplot as plt
from acoustics import Signal

def file_path_to_img(file_path):
    img = open(file_path, 'rb').read()
    img = base64.b64encode(img)
    return img.decode('utf-8')

def load_files(wav_names, start_dur):
    lib_list = []
    sig_list = []
    if not wav_names:
        lib_list = None
    else:
        for idx, wav_name in enumerate(wav_names):
            lib_data_temp, lib_sr_temp = librosa.load(wav_name, sr=None)
            sig_temp = Signal.from_wav(wav_name)
            start_dur[idx][0] = start_dur[idx][0] if start_dur[idx][0] and start_dur[idx][0] < float(len(lib_data_temp))/lib_sr_temp and start_dur[idx][0] > 0 else 0
            start_dur[idx][1] = start_dur[idx][1] if start_dur[idx][1] and start_dur[idx][1] < float(len(lib_data_temp))/lib_sr_temp - start_dur[idx][0] and start_dur[idx][1] > 0 else float(len(lib_data_temp))/lib_sr_temp - start_dur[idx][0]

            lib_time_data, lib_time_samplerate = librosa.load(wav_name, sr=None, offset=start_dur[idx][0], duration=start_dur[idx][1])
            lib_list_temp = [lib_time_samplerate, lib_time_data]
            lib_list.append(lib_list_temp)
            sig_list.append(sig_temp)
    return lib_list, start_dur, sig_list

def normalize_signals(sig_lib_list, sig_start_dur, sig_sig_list, ref_lib_list=None, ref_start_dur=None, ref_sig_list=None):
    if ref_lib_list == None:
        return sig_lib_list, sig_start_dur, sig_sig_list
    else:
        return ref_lib_list, ref_start_dur, ref_sig_list

def get_graph(temp_spec, attr, mic_Data_Record):
    full_name = 'Uploads/' + temp_spec + '/' + attr + '/' + attr + '_' + str(mic_Data_Record.pk) + '.png'
    if os.path.exists(full_name):
        os.remove(full_name)
    plt.savefig(full_name)
    return full_name

def charts_preprocess(sig_wav_names, start_dur, ref_wav_names=None):
    plt.switch_backend('AGG')
    sig_dur_list = []
    ref_dur_list = []
    for i in enumerate(start_dur):
        sig_dur_list.append([
            start_dur[i[0]][0] if start_dur[i[0]][0] else None,
            start_dur[i[0]][2] if start_dur[i[0]][2] else None
        ])
        ref_dur_list.append([
            start_dur[i[0]][1] if start_dur[i[0]][1] else None,
            start_dur[i[0]][2] if start_dur[i[0]][2] else None
        ])
    sig_lib_list, clean_sig_dur, sig_sig_list = load_files(sig_wav_names, sig_dur_list)
    ref_lib_list, clean_ref_dur, ref_sig_list = load_files(ref_wav_names, ref_dur_list)
    norm_lib_list, norm_start_dur, norm_sig_list = normalize_signals(sig_lib_list, clean_sig_dur, sig_sig_list, ref_lib_list, clean_ref_dur, ref_sig_list)
    
    return norm_lib_list, norm_start_dur, norm_sig_list