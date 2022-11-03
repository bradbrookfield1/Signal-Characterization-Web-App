import base64, sys
from io import BytesIO
import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile
from scipy import signal
import librosa
import librosa.display

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

def get_signal_charts(lib_list, dur_list):
    sig_chart_list = []
    if lib_list:
        for idx, lib_entry in enumerate(lib_list):
            plt.figure(1, figsize=(4, 3)).clf()
            librosa.display.waveshow(lib_entry[1], sr=lib_entry[0], max_points=sys.maxsize, offset=dur_list[idx][0])
            plt.title('Time Domain Original Signal')
            plt.xlabel('Time [s]')
            plt.ylabel('Amplitude')
            plt.tight_layout()
            sig_chart_list.append(get_graph())
    return sig_chart_list

def get_PSD_charts(lib_list):    
    psd_chart_list = []
    if lib_list:
        for lib_entry in lib_list:            
            psd_freq, psd_data = signal.welch(x=lib_entry[1], fs=lib_entry[0])
            plt.figure(1, figsize=(4, 3)).clf()
            plt.loglog(psd_freq, psd_data, lw=1, label='Bruh')
            plt.plot([250, 250], [1e-7, 1e16], 'r', lw=3, label='250 Hz')
            plt.legend()
            plt.title('Power Spectral Density')
            plt.xlabel('Frequency')
            plt.ylabel('PSD')
            plt.tight_layout()
            psd_chart_list.append(get_graph())
    return psd_chart_list

def get_spectrograms(lib_list):
    spec_chart_list = []
    if lib_list:
        for idx, lib_entry in enumerate(lib_list):
            spec_fft_data = librosa.stft(lib_list[idx][1])
            spec_fft_db_data = librosa.amplitude_to_db(abs(spec_fft_data), ref=2e-5)
            plt.figure(1, figsize=(4, 3)).clf()
            librosa.display.specshow(
                spec_fft_db_data,
                sr=lib_list[idx][0],
                x_axis='time',
                y_axis='log',
            )
            plt.colorbar(format="%+2.f dB")
            
            plt.plot([0, float(len(lib_entry[1]))/lib_entry[0]], [250, 250], 'g', lw=3)
            plt.title('Spectrogram')
            plt.tight_layout()
            spec_chart_list.append(get_graph())
    return spec_chart_list

def normalize_signals(sig_lib_list, ref_lib_list=None):
    if ref_lib_list == None:
        return sig_lib_list
    else:
        return ref_lib_list

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_charts_detail(chart_indicator, sig_wav_names, start_dur, ref_wav_names=None):
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
    norm_lib_list = normalize_signals(sig_lib_list, ref_lib_list)
    match chart_indicator:
        case 'All':
            signal_graphs = get_signal_charts(norm_lib_list, clean_sig_dur)
            psd_graphs = get_PSD_charts(norm_lib_list)
            spectrograms = get_spectrograms(norm_lib_list)
        case 'Time Signal':
            signal_graphs = get_signal_charts(norm_lib_list, clean_sig_dur)
            psd_graphs = None
            spectrograms = None
        case 'PSD':
            signal_graphs = None
            psd_graphs = get_PSD_charts(norm_lib_list)
            spectrograms = None
        case 'Spectrogram':
            signal_graphs = None
            psd_graphs = None
            spectrograms = get_spectrograms(norm_lib_list)
    return signal_graphs, psd_graphs, spectrograms