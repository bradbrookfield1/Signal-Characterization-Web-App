import base64, time, sys
from io import BytesIO
import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile
from scipy import signal
import librosa
import librosa.display

def load_files(wav_names, start_dur):
    wav_list = []
    lib_list = []
    if not wav_names:
        wav_list = None
        lib_list = None
    else:
        for idx, wav_name in enumerate(wav_names):
            try:
                with open(wav_name, 'rb') as fd:
                    contents = fd.read()
                wav_name = BytesIO(contents)
                wav_time_samplerate, wav_time_data = wavfile.read(wav_name)
            except IOError:
                sys.exit('Error reading wav file!')
            lib_time_data, lib_time_samplerate = librosa.load(wav_name, sr=None, offset=start_dur[idx][0], duration=start_dur[idx][1])
            # lib_time_t = [range(start_dur[idx][sig_ref_idx], start_dur[idx][sig_ref_idx] + start_dur[idx][sig_ref_idx + 1] + 1, 1)]
            wav_list_temp = [wav_time_samplerate, wav_time_data]
            lib_list_temp = [lib_time_samplerate, lib_time_data]
            wav_list.append(wav_list_temp)
            lib_list.append(lib_list_temp)
    return wav_list, lib_list

def get_signal_charts(lib_list, dur_list):
    sig_chart_list = []
    if lib_list:
        for idx, lib_entry in enumerate(lib_list):
            dur_list[idx][0] = dur_list[idx][0] if dur_list[idx][0] and not dur_list[idx][0] > len(lib_entry[1]) else 0
            plt.figure(1, figsize=(4, 3)).clf()
            # Takes longer, but works for all signals.
            # start = time.time()
            # librosa.display.waveshow(lib_entry[1], sr=lib_entry[0], max_points=sys.maxsize)
            librosa.display.waveshow(lib_entry[1], sr=lib_entry[0], max_points=sys.maxsize, offset=dur_list[idx][0])
            # print(round(time.time() - start, 5))
            
            # Quicker, but doesn't work for all signals.
            # start = time.time()
            # time_length = float(len(lib_entry[1])) / lib_entry[0]
            # time_t = np.linspace(0., time_length, len(lib_entry[1]))
            # plt.plot(time_t, lib_entry[1], lw=1)
            # print(round(time.time() - start, 5))
            
            plt.title('Time Domain Original Signal')
            plt.xlabel('Time [s]')
            plt.ylabel('Amplitude')
            plt.tight_layout()
            sig_chart_list.append(get_graph())
    return sig_chart_list

def get_PSD_charts(wav_list):    
    psd_chart_list = []
    if wav_list:
        for wav_entry in wav_list:
            psd_freq, psd_data = signal.welch(x=wav_entry[1], fs=wav_entry[0])
            step = 1/len(psd_data)
            psd_freq = range(psd_freq[0], psd_freq[1], step)
            plt.figure(1, figsize=(4, 3)).clf()
            plt.loglog(psd_freq, psd_data, lw=1, label='Bruh')
            plt.plot([250, 250], [1e-7, 1e16], 'r', lw=3, label='250 Hz')
            plt.legend()
            plt.ylim(1e5, 1e16)
            plt.title('Power Spectral Density')
            plt.xlabel('Frequency')
            plt.ylabel('PSD')
            plt.tight_layout()
            psd_chart_list.append(get_graph())
    return psd_chart_list

def get_spectrograms(wav_list, lib_list, dur_list):
    spec_chart_list = []
    if lib_list:
        for idx, lib_entry in enumerate(lib_list):
            dur_list[idx][0] = dur_list[idx][0] if dur_list[idx][0] else 0
            dur_list[idx][1] = dur_list[idx][1] if dur_list[idx][1] else (len(lib_entry[1]) - dur_list[idx][0])/lib_entry[0]
            spec_fft_data = librosa.stft(lib_list[idx][1])
            spec_fft_db_data = librosa.amplitude_to_db(abs(spec_fft_data), ref=2e-5)
            
            plt.figure(1, figsize=(4, 3)).clf()
            librosa.display.specshow(
                spec_fft_db_data,
                sr=lib_list[idx][0],
                x_axis='time',
                y_axis='log',
                # tmin=dur_list[idx][0] if dur_list[idx][0] else None,
                # tmax=dur_list[idx][0] + dur_list[idx][1] if dur_list[idx][1] else None
            )
            plt.colorbar(format="%+2.f dB")
            # plt.xlim([dur_list[idx][0], dur_list[idx][0] + dur_list[idx][1]])
            
            # locs, labels = plt.xticks()
            # for i in range(len(labels)):
            #     labels[i] = labels[i] + dur_list[idx][0]
            
            # time_length = float(dur_list[idx][1]) / lib_entry[0]
            # time_t = np.arange(dur_list[idx][0], dur_list[idx][0] + dur_list[idx][1] + 1, time_length)
            
            # time_length = float(len(wav_entry[1])) / wav_entry[0]
            # time_t = np.linspace(0., time_length, len(wav_entry[1]))
            # plt.plot([0, time_length*lib_entry[0]], [250, 250], 'g', lw=3)
            plt.plot([0, float(len(lib_entry[1]))/lib_entry[0]], [250, 250], 'g', lw=3)
            plt.title('Spectrogram')
            plt.tight_layout()
            spec_chart_list.append(get_graph())
    return spec_chart_list

def normalize_signals(sig_wav_list, sig_lib_list, ref_wav_list=None, ref_lib_list=None):
    if ref_wav_list == None:
        return sig_wav_list, sig_lib_list
    else:
        return ref_wav_list, ref_lib_list

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
    for i, std in enumerate(start_dur):
        sig_dur_list.append([
            # start_dur[i[0]][0] if not start_dur[i[0]][0] == None else None,
            # start_dur[i[0]][1] if not start_dur[i[0]][1] == None else None
            start_dur[i][0] if not start_dur[i][0] == None else None,
            start_dur[i][2] if not start_dur[i][2] == None else None
        ])
        ref_dur_list.append([
            # start_dur[i[0]][1] if not start_dur[i[0]][1] == None else None,
            # start_dur[i[0]][2] if not start_dur[i[0]][2] == None else None
            start_dur[i][1] if not start_dur[i][1] == None else None,
            start_dur[i][2] if not start_dur[i][2] == None else None
        ])
    sig_wav_list, sig_lib_list = load_files(sig_wav_names, sig_dur_list)
    ref_wav_list, ref_lib_list = load_files(ref_wav_names, ref_dur_list)
    norm_wav_list, norm_lib_list = normalize_signals(sig_wav_list, sig_lib_list, ref_wav_list, ref_lib_list)
    match chart_indicator:
        case 'All':
            signal_graphs = get_signal_charts(norm_lib_list, sig_dur_list)
            # psd_graphs = get_PSD_charts(norm_wav_list)
            psd_graphs = None
            spectrograms = get_spectrograms(norm_wav_list, norm_lib_list, sig_dur_list)
        case 'Time Signal':
            signal_graphs = get_signal_charts(norm_lib_list, sig_dur_list)
            psd_graphs = None
            spectrograms = None
        case 'PSD':
            signal_graphs = None
            # psd_graphs = get_PSD_charts(norm_wav_list)
            psd_graphs = None
            spectrograms = None
        case 'Spectrogram':
            signal_graphs = None
            psd_graphs = None
            spectrograms = get_spectrograms(norm_wav_list, norm_lib_list, sig_dur_list)
    return signal_graphs, psd_graphs, spectrograms