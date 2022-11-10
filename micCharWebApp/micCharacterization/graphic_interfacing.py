import base64
from io import BytesIO
import librosa
from matplotlib import pyplot as plt

def load_files(wav_names, start_dur):
    lib_list = []
    if not wav_names:
        lib_list = None
    else:
        for idx, wav_name in enumerate(wav_names):
            lib_data_temp, lib_sr_temp = librosa.load(wav_name, sr=None)
            start_dur[idx][0] = start_dur[idx][0] if start_dur[idx][0] and start_dur[idx][0] < float(len(lib_data_temp))/lib_sr_temp and start_dur[idx][0] > 0 else 0
            start_dur[idx][1] = start_dur[idx][1] if start_dur[idx][1] and start_dur[idx][1] < float(len(lib_data_temp))/lib_sr_temp - start_dur[idx][0] and start_dur[idx][1] > 0 else float(len(lib_data_temp))/lib_sr_temp - start_dur[idx][0]

            lib_time_data, lib_time_samplerate = librosa.load(wav_name, sr=None, offset=start_dur[idx][0], duration=start_dur[idx][1])
            lib_list_temp = [lib_time_samplerate, lib_time_data]
            lib_list.append(lib_list_temp)
    return lib_list, start_dur

def normalize_signals(sig_lib_list, sig_start_dur, ref_lib_list=None, ref_start_dur=None):
    if ref_lib_list == None:
        return sig_lib_list, sig_start_dur
    else:
        return ref_lib_list, ref_start_dur

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def charts_preprocess(sig_wav_names, start_dur, ref_wav_names=None):
    plt.switch_backend('AGG')
    sig_dur_list = []
    ref_dur_list = []
    for i in enumerate(start_dur):
        sig_dur_list.append([
            start_dur[i[0]][0] if not start_dur[i[0]][0] == None else None,
            start_dur[i[0]][2] if not start_dur[i[0]][2] == None else None
        ])
        ref_dur_list.append([
            start_dur[i[0]][1] if not start_dur[i[0]][1] == None else None,
            start_dur[i[0]][2] if not start_dur[i[0]][2] == None else None
        ])
    sig_lib_list, clean_sig_dur = load_files(sig_wav_names, sig_dur_list)
    ref_lib_list, clean_ref_dur = load_files(ref_wav_names, ref_dur_list)
    norm_lib_list, norm_start_dur = normalize_signals(sig_lib_list, clean_sig_dur, ref_lib_list, clean_ref_dur)
    return norm_lib_list, norm_start_dur