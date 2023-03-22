from django.core.files.base import File
from temporalDatabase import graphs as temp
from spectralDatabase import graphs as spec
from snrDatabase import graphs as snr
from statisticalDatabase import graphs as stat
from .models import MicDataRecord
from temporalDatabase.models import TemporalDatabase
from spectralDatabase.models import SpectralDatabase
from snrDatabase.models import SNRDatabase
from statisticalDatabase.models import StatisticalDatabase
import soundfile as sf
import pandas as pd
import numpy as np
from .preprocessing import charts_preprocess, apply_norm
from . import graphs_propagation
from .calculations import get_SNR_arrays, db_array_to_mean
from .constants import tunnel_dist, dist_array_lin, dist_array_log, dist_array_big
from .constants import p_bar_array, p_ref, window
from matplotlib import pyplot as plt
from scipy import signal
from librosa import A_weighting, C_weighting, stft, istft, decompose, onset
import copy, os, wave

def help_get_context():
    file_set_list = MicDataRecord.get_fileset()
    records = MicDataRecord.objects.all().order_by('pk')
    name_list = []
    for record in records:
        name_list.append(record.record_Name)
    return file_set_list, name_list, records

def spec_prop_abs_coeff_graphs():
    plt.switch_backend('AGG')
    return [graphs_propagation.prop_snr_pred_dist(dist_array_lin),
            snr.get_avg_snr_vs_dist(dist_array_big),
            graphs_propagation.get_spec_prop_abs_coeff_hum(),
            graphs_propagation.get_spec_prop_abs_coeff_temp(),
            graphs_propagation.get_spec_prop_abs_coeff_dist(dist_array_lin),
            graphs_propagation.get_spec_prop_abs_coeff_dist(dist_array_log),
            graphs_propagation.get_spec_prop_abs_coeff_p(p_bar_array, p_ref),
            graphs_propagation.get_spec_prop_abs_coeff_p(p_bar_array, p_bar_array)]

def get_hpss_audio(lib_sig):
    lib_sig_fft = stft(lib_sig)
    harm, perc = decompose.hpss(lib_sig_fft)
    harm_sig = istft(harm)
    perc_sig = istft(perc)
    return harm_sig, perc_sig

def save_hpss_files(obj, file_paths, file_names):
    file_fields_short = ['noisy_Signal', 'measured_Signal', 'noise', 'true_Signal']
    sound_list = charts_preprocess(file_paths)
    for typ, sound, nam in zip(file_fields_short, sound_list, file_names):
        if sound:
            harm, perc = get_hpss_audio(sound[0][1])
            sf.write('./Uploads/Recordings/Temp/Harmonics/' + nam, harm, sound[0][0])
            sf.write('./Uploads/Recordings/Temp/Percussives/' + nam, perc, sound[0][0])
            
            with open('./Uploads/Recordings/Temp/Harmonics/' + nam, 'rb') as f:
                exec('obj.' + typ + '_Harmonics.save(nam, File(f))')
            with open('./Uploads/Recordings/Temp/Percussives/' + nam, 'rb') as f:
                exec('obj.' + typ + '_Percussives.save(nam, File(f))')

            if os.path.exists('./Uploads/Recordings/Temp/Harmonics/' + nam):
                os.remove('./Uploads/Recordings/Temp/Harmonics/' + nam)
            if os.path.exists('./Uploads/Recordings/Temp/Percussives/' + nam):
                os.remove('./Uploads/Recordings/Temp/Percussives/' + nam)

def list_intro(db_type):
    file_set_list, name_list, records = help_get_context()
    norm_noisy_sig_list = []
    norm_sig_list = []
    norm_noise_list = []
    true_sig_list = []
    for file_set in file_set_list:
        norm_noisy_sig, norm_sig, norm_noise, true_sig = charts_preprocess(file_set)
        norm_noisy_sig_list.append(norm_noisy_sig)
        norm_sig_list.append(norm_sig)
        norm_noise_list.append(norm_noise)
        true_sig_list.append(true_sig)
    if db_type == 'Temporal':
        db = TemporalDatabase.objects.all().order_by('pk')
    elif db_type == 'Spectral':
        db = SpectralDatabase.objects.all().order_by('pk')
    elif db_type == 'SNR':
        db = SNRDatabase.objects.all().order_by('pk')
    else:
        db = StatisticalDatabase.objects.all().order_by('pk')
    return norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db

def detail_intro(context, mic_Data_Record):
    record_DB_dict = mic_Data_Record.__dict__
    record_DB_dict_fixed = copy.deepcopy(record_DB_dict)
    del record_DB_dict_fixed['record_Name'], record_DB_dict_fixed['description'], record_DB_dict_fixed['prediction_Harmonics']
    del record_DB_dict_fixed['noisy_Signal_Harmonics'], record_DB_dict_fixed['measured_Signal_Harmonics']
    del record_DB_dict_fixed['noise_Harmonics'], record_DB_dict_fixed['true_Signal_Harmonics']
    del record_DB_dict_fixed['noisy_Signal_Percussives'], record_DB_dict_fixed['measured_Signal_Percussives']
    del record_DB_dict_fixed['noise_Percussives'], record_DB_dict_fixed['true_Signal_Percussives']
    del record_DB_dict_fixed['_state'], record_DB_dict_fixed['id']
    file_list = []
    for attr, value in record_DB_dict_fixed.items():
        if mic_Data_Record.filename(attr):
            context[attr] = mic_Data_Record.filename(attr)
            file_list.append('./Uploads/Recordings/Original/' + attr + '/' + context[attr])
        else:
            context[attr] = None
            file_list.append(None)
    norm_noisy_sig, norm_sig, norm_noise, true_sig = charts_preprocess(file_list)
    
    temp_DB = TemporalDatabase.objects.filter(mic_Data_Record=mic_Data_Record).get()
    spec_DB = SpectralDatabase.objects.filter(mic_Data_Record=mic_Data_Record).get()
    snr_DB = SNRDatabase.objects.filter(mic_Data_Record=mic_Data_Record).get()
    stat_DB = StatisticalDatabase.objects.filter(mic_Data_Record=mic_Data_Record).get()
    temp_DB_dict = temp_DB.__dict__
    spec_DB_dict = spec_DB.__dict__
    snr_DB_dict = snr_DB.__dict__
    stat_DB_dict = stat_DB.__dict__
    temp_DB_dict_fixed = copy.deepcopy(temp_DB_dict)
    spec_DB_dict_fixed = copy.deepcopy(spec_DB_dict)
    snr_DB_dict_fixed = copy.deepcopy(snr_DB_dict)
    stat_DB_dict_fixed = copy.deepcopy(stat_DB_dict)
    del temp_DB_dict_fixed['_state'], temp_DB_dict_fixed['id'], temp_DB_dict_fixed['mic_Data_Record_id']
    del spec_DB_dict_fixed['_state'], spec_DB_dict_fixed['id'], spec_DB_dict_fixed['mic_Data_Record_id']
    del spec_DB_dict_fixed['harmonic_Prediction_Graph']
    del snr_DB_dict_fixed['_state'], snr_DB_dict_fixed['id'], snr_DB_dict_fixed['mic_Data_Record_id']
    del stat_DB_dict_fixed['_state'], stat_DB_dict_fixed['id'], stat_DB_dict_fixed['mic_Data_Record_id']
    return context, norm_noisy_sig, norm_sig, norm_noise, true_sig, temp_DB_dict_fixed, spec_DB_dict_fixed, snr_DB_dict_fixed, stat_DB_dict_fixed, temp_DB, spec_DB, snr_DB, stat_DB

def delete_intro(mic_Data_Record):
    temp_DB = TemporalDatabase.objects.filter(mic_Data_Record=mic_Data_Record).get()
    spec_DB = SpectralDatabase.objects.filter(mic_Data_Record=mic_Data_Record).get()
    snr_DB = SNRDatabase.objects.filter(mic_Data_Record=mic_Data_Record).get()
    stat_DB = StatisticalDatabase.objects.filter(mic_Data_Record=mic_Data_Record).get()
    temp_DB_dict_fixed = temp_DB.__dict__
    spec_DB_dict_fixed = spec_DB.__dict__
    snr_DB_dict_fixed = snr_DB.__dict__
    stat_DB_dict_fixed = stat_DB.__dict__
    del temp_DB_dict_fixed['_state'], temp_DB_dict_fixed['id'], temp_DB_dict_fixed['mic_Data_Record_id']
    del spec_DB_dict_fixed['_state'], spec_DB_dict_fixed['id'], spec_DB_dict_fixed['mic_Data_Record_id']
    del spec_DB_dict_fixed['harmonic_Prediction_Graph']
    del snr_DB_dict_fixed['_state'], snr_DB_dict_fixed['id'], snr_DB_dict_fixed['mic_Data_Record_id']
    del stat_DB_dict_fixed['_state'], stat_DB_dict_fixed['id'], stat_DB_dict_fixed['mic_Data_Record_id']
    return temp_DB_dict_fixed, spec_DB_dict_fixed, snr_DB_dict_fixed, stat_DB_dict_fixed

def find_graph(graph_type, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record=None, hpss_array=None):
    stat_norm = True
    if norm_noisy_sig:
        plot_me = norm_noisy_sig
    elif norm_sig:
        plot_me = norm_sig
    elif norm_noise:
        plot_me = norm_noise
    else:
        plot_me = true_sig
    match graph_type:
        case 'signal_Graph':
            context[graph_type] = temp.get_signal(plot_me[0], plot_me[1], name, mic_Data_Record)
        case 'cepstrum_Graph':
            context[graph_type] = temp.get_cepstrum(plot_me[0], plot_me[1], name, mic_Data_Record)
        case 'hilbert_Phase_Graph':
            context[graph_type] = temp.get_inst_phase(plot_me[0], plot_me[1], name, mic_Data_Record)
        case 'onset_Strength_Graph':
            context[graph_type] = temp.get_onset_strength(plot_me[0], name, mic_Data_Record)
        case 'lag_Autocorrelation_Graph':
            context[graph_type] = temp.get_lag_autocorrelation(plot_me[0], name, mic_Data_Record)
        case 'BPM_Autocorrelation_Graph':
            context[graph_type] = temp.get_bpm_autocorrelation(plot_me[0], name, mic_Data_Record)
        case 'autocorrelation_Tempogram':
            context[graph_type] = temp.get_autocorr_tempogram(plot_me[0], name, mic_Data_Record)
        case 'fourier_Tempogram':
            context[graph_type] = temp.get_fourier_tempogram(plot_me[0], name, mic_Data_Record)
        case 'average_PSD_Graph':
            context[graph_type] = spec.get_PSD(plot_me[2], name, mic_Data_Record)
        case 'phase_Spectrum_Graph':
            context[graph_type] = spec.get_phase_spectrum(plot_me[1], name, mic_Data_Record)
        case 'pure_Signal_SNR_Graph':
            context[graph_type] = snr.get_SNR(norm_sig[2], norm_noise[2], 'Given Signal and Noise', graph_type, name, mic_Data_Record) if norm_sig and norm_noise else None
        case 'system_Signal_SNR_Graph':
            context[graph_type] = snr.get_SNR(true_sig[2], norm_noisy_sig[2], 'System Approach', graph_type, name, mic_Data_Record) if true_sig and norm_noisy_sig else None
        case 'given_Signal_SNR_Graph':
            context[graph_type] = snr.get_SNR(norm_sig[2], norm_noisy_sig[2], 'Given Signal', graph_type, name, mic_Data_Record) if norm_sig and norm_noisy_sig else None
        case 'given_Noise_SNR_Graph':
            context[graph_type] = snr.get_SNR(norm_noisy_sig[2], norm_noise[2], 'Given Noise', graph_type, name, mic_Data_Record) if norm_noisy_sig and norm_noise else None
        case 'average_SNR_Distance_Graph':
            db_rolled_both = []
            if norm_sig and norm_noise:
                weight_freqs, _, _, db_rolled_both = get_SNR_arrays(norm_sig[2], norm_noise[2], 'Given Signal and Noise')
            elif norm_sig and norm_noisy_sig:
                weight_freqs, _, _, db_rolled_both = get_SNR_arrays(norm_sig[2], norm_noisy_sig[2], 'Given Signal')
            elif norm_noisy_sig and norm_noise:
                weight_freqs, _, _, db_rolled_both = get_SNR_arrays(norm_noisy_sig[2], norm_noise[2], 'Given Noise')
            elif true_sig and norm_noisy_sig:
                weight_freqs, _, _, db_rolled_both = get_SNR_arrays(true_sig[2], norm_noisy_sig[2], 'System Approach')

            if len(db_rolled_both) == 0:
                context[graph_type] = None
            else:
                db_rolled_both = db_rolled_both[(window - 1):(-window + 1)]
                a_weight = A_weighting(weight_freqs)[(window - 1):(-window + 1)]
                c_weight = C_weighting(weight_freqs)[(window - 1):(-window + 1)]
                db_rolled_avg = db_array_to_mean(db_rolled_both - c_weight + a_weight)
                context[graph_type] = snr.get_avg_snr_vs_dist(dist_array_big, name, mic_Data_Record, db_rolled_avg, tunnel_dist)
        case 'spectrogram':
            context[graph_type] = spec.get_spectrogram(plot_me[0], name, mic_Data_Record)
        case 'mellin_Spectrogram':
            context[graph_type] = spec.get_mellin(plot_me[0], name, mic_Data_Record)
        case 'percussive_Spectrogram':
            context[graph_type] = spec.get_percussive(plot_me[0], name, mic_Data_Record)
        case 'harmonic_Spectrogram':
            context[graph_type] = spec.get_harmonic(plot_me[0], name, mic_Data_Record)
        case 'harmonic_Prediction_Graph':
            context[graph_type] = spec.get_harmonic_prediction(plot_me[0], mic_Data_Record.prediction_Harmonics, name, mic_Data_Record)
        case 'original_PDF_Graph':
            if norm_noisy_sig and norm_noise:
                ns = [norm_noisy_sig[0][0], apply_norm(norm_noisy_sig[0][1])] if stat_norm == True else norm_noisy_sig[0]
                n = [norm_noise[0][0], apply_norm(norm_noise[0][1])] if stat_norm == True else norm_noise[0]
                context[graph_type] = stat.get_original_PDFs(ns, n, 'Original', graph_type, name, mic_Data_Record) if norm_noisy_sig and norm_noise else None
            else:
                context[graph_type] = None
        case 'harmonic_HPSS_PDF_Graph':
            if norm_noisy_sig and norm_noise:
                ns = [norm_noisy_sig[0][0], apply_norm(norm_noisy_sig[0][1])] if stat_norm == True else norm_noisy_sig[0]
                n = [norm_noise[0][0], apply_norm(norm_noise[0][1])] if stat_norm == True else norm_noise[0]
                context[graph_type] = stat.get_original_PDFs(ns, n, 'Harmonic HPSS', graph_type, name, mic_Data_Record, hpss_array, stat_norm) if norm_noisy_sig and norm_noise and hpss_array else None
            else:
                context[graph_type] = None
        case 'percussive_HPSS_PDF_Graph':
            if norm_noisy_sig and norm_noise:
                ns = [norm_noisy_sig[0][0], apply_norm(norm_noisy_sig[0][1])] if stat_norm == True else norm_noisy_sig[0]
                n = [norm_noise[0][0], apply_norm(norm_noise[0][1])] if stat_norm == True else norm_noise[0]
                context[graph_type] = stat.get_original_PDFs(ns, n, 'Percussive HPSS', graph_type, name, mic_Data_Record, hpss_array, stat_norm) if norm_noisy_sig and norm_noise and hpss_array else None
            else:
                context[graph_type] = None
        case 'welch_PDF_Graph':
            if norm_noisy_sig and norm_noise:
                ns = [norm_noisy_sig[0][0], apply_norm(norm_noisy_sig[0][1])] if stat_norm == True else norm_noisy_sig[0]
                n = [norm_noise[0][0], apply_norm(norm_noise[0][1])] if stat_norm == True else norm_noise[0]
                noisy_sig_welch = [ns[0], pd.Series(signal.welch(ns[1], fs=ns[0], average='mean')[1]).rolling(13, center=True).mean().to_numpy()]
                noise_welch = [n[0], pd.Series(signal.welch(n[1], fs=n[0], average='mean')[1]).rolling(13, center=True).mean().to_numpy()]
                context[graph_type] = stat.get_original_PDFs(noisy_sig_welch, noise_welch, 'Welch', graph_type, name, mic_Data_Record) if norm_noisy_sig and norm_noise else None
            else:
                context[graph_type] = None
        case 'magnitude_FFT_Spectrum_Graph':
            if norm_noisy_sig and norm_noise:
                ns = [norm_noisy_sig[0][0], np.float32(apply_norm(norm_noisy_sig[0][1]))] if stat_norm == True else norm_noisy_sig[0]
                n = [norm_noise[0][0], np.float32(apply_norm(norm_noise[0][1]))] if stat_norm == True else norm_noise[0]
                context[graph_type] = stat.get_fft_PDFs(ns, n, 'Magnitude FFT Spectrum', graph_type, name, mic_Data_Record) if norm_noisy_sig and norm_noise else None
            else:
                context[graph_type] = None
        case 'magnitude_FFT_Time_Graph':
            if norm_noisy_sig and norm_noise:
                ns = [norm_noisy_sig[0][0], np.float32(apply_norm(norm_noisy_sig[0][1]))] if stat_norm == True else norm_noisy_sig[0]
                n = [norm_noise[0][0], np.float32(apply_norm(norm_noise[0][1]))] if stat_norm == True else norm_noise[0]
                context[graph_type] = stat.get_fft_PDFs(ns, n, 'Magnitude FFT Time', graph_type, name, mic_Data_Record) if norm_noisy_sig and norm_noise else None
            else:
                context[graph_type] = None
        case 'phase_FFT_Spectrum_Graph':
            if norm_noisy_sig and norm_noise:
                ns = [norm_noisy_sig[0][0], np.float32(apply_norm(norm_noisy_sig[0][1]))] if stat_norm == True else norm_noisy_sig[0]
                n = [norm_noise[0][0], np.float32(apply_norm(norm_noise[0][1]))] if stat_norm == True else norm_noise[0]
                context[graph_type] = stat.get_fft_PDFs(ns, n, 'Phase FFT Spectrum', graph_type, name, mic_Data_Record) if norm_noisy_sig and norm_noise else None
            else:
                context[graph_type] = None
        case 'phase_FFT_Time_Graph':
            if norm_noisy_sig and norm_noise:
                ns = [norm_noisy_sig[0][0], np.float32(apply_norm(norm_noisy_sig[0][1]))] if stat_norm == True else norm_noisy_sig[0]
                n = [norm_noise[0][0], np.float32(apply_norm(norm_noise[0][1]))] if stat_norm == True else norm_noise[0]
                context[graph_type] = stat.get_fft_PDFs(ns, n, 'Phase FFT Time', graph_type, name, mic_Data_Record) if norm_noisy_sig and norm_noise else None
            else:
                context[graph_type] = None
        case 'magnitude_FMT_Spectrum_Graph':
            if norm_noisy_sig and norm_noise:
                ns = [norm_noisy_sig[0][0], np.float32(apply_norm(norm_noisy_sig[0][1]))] if stat_norm == True else norm_noisy_sig[0]
                n = [norm_noise[0][0], np.float32(apply_norm(norm_noise[0][1]))] if stat_norm == True else norm_noise[0]
                context[graph_type] = stat.get_fft_PDFs(ns, n, 'Magnitude Mellin Spectrum', graph_type, name, mic_Data_Record) if norm_noisy_sig and norm_noise else None
            else:
                context[graph_type] = None
        case 'magnitude_FMT_Time_Graph':
            if norm_noisy_sig and norm_noise:
                ns = [norm_noisy_sig[0][0], np.float32(apply_norm(norm_noisy_sig[0][1]))] if stat_norm == True else norm_noisy_sig[0]
                n = [norm_noise[0][0], np.float32(apply_norm(norm_noise[0][1]))] if stat_norm == True else norm_noise[0]
                context[graph_type] = stat.get_fft_PDFs(ns, n, 'Magnitude Mellin Time', graph_type, name, mic_Data_Record) if norm_noisy_sig and norm_noise else None
            else:
                context[graph_type] = None
        case 'phase_FMT_Spectrum_Graph':
            if norm_noisy_sig and norm_noise:
                ns = [norm_noisy_sig[0][0], np.float32(apply_norm(norm_noisy_sig[0][1]))] if stat_norm == True else norm_noisy_sig[0]
                n = [norm_noise[0][0], np.float32(apply_norm(norm_noise[0][1]))] if stat_norm == True else norm_noise[0]
                context[graph_type] = stat.get_fft_PDFs(ns, n, 'Phase Mellin Spectrum', graph_type, name, mic_Data_Record) if norm_noisy_sig and norm_noise else None
            else:
                context[graph_type] = None
        case 'phase_FMT_Time_Graph':
            if norm_noisy_sig and norm_noise:
                ns = [norm_noisy_sig[0][0], np.float32(apply_norm(norm_noisy_sig[0][1]))] if stat_norm == True else norm_noisy_sig[0]
                n = [norm_noise[0][0], np.float32(apply_norm(norm_noise[0][1]))] if stat_norm == True else norm_noise[0]
                context[graph_type] = stat.get_fft_PDFs(ns, n, 'Phase Mellin Time', graph_type, name, mic_Data_Record) if norm_noisy_sig and norm_noise else None
            else:
                context[graph_type] = None
        case 'hilbert_PDF_Graph':
            if norm_noisy_sig and norm_noise:
                context[graph_type] = stat.get_Signal_PDFs([norm_noisy_sig[0][0], norm_noisy_sig[1]], [norm_noise[0][0], norm_noise[1]], 'Hilbert Transform', graph_type, name, mic_Data_Record) if norm_noisy_sig and norm_noise else None
            else:
                context[graph_type] = None
        case 'onset_Strength_PDF_Graph':
            if norm_noisy_sig and norm_noise:
                ns = [norm_noisy_sig[0][0], np.float32(apply_norm(norm_noisy_sig[0][1]))] if stat_norm == True else norm_noisy_sig[0]
                n = [norm_noise[0][0], np.float32(apply_norm(norm_noise[0][1]))] if stat_norm == True else norm_noise[0]
                ns_os = onset.onset_strength(y=ns[1], sr=ns[0])
                norm_ns_os = ns_os/(ns_os.max())
                n_os = onset.onset_strength(y=n[1], sr=n[0])
                norm_n_os = n_os/(n_os.max())
                context[graph_type] = stat.get_original_PDFs(norm_ns_os, norm_n_os, 'Onset Strength', graph_type, name, mic_Data_Record) if norm_noisy_sig and norm_noise else None
            else:
                context[graph_type] = None
        case 'inst_Phase_PDF_Graph':
            if norm_noisy_sig and norm_noise:
                ns = [norm_noisy_sig[0][0], apply_norm(norm_noisy_sig[0][1])] if stat_norm == True else norm_noisy_sig[0]
                n = [norm_noise[0][0], apply_norm(norm_noise[0][1])] if stat_norm == True else norm_noise[0]
                context[graph_type] = stat.get_Signal_PDFs(ns, n, 'Instantaneous Phase', graph_type, name, mic_Data_Record) if norm_noisy_sig and norm_noise else None
            else:
                context[graph_type] = None
    return context