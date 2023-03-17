from .models import MicDataRecord
from temporalDatabase.models import TemporalDatabase
from spectralDatabase.models import SpectralDatabase
from snrDatabase.models import SNRDatabase
from statisticalDatabase.models import StatisticalDatabase
from .preprocessing import charts_preprocess
from . import graphs_snr_prop, graphs_temporal, graphs_spectral
from .calculations import get_SNR_arrays, db_array_to_mean
from .constants import distance, tunnel_dist, dist_array_lin, dist_array_log, dist_array_big
from .constants import p_bar_array, p_ref, window
from matplotlib import pyplot as plt
from librosa import A_weighting, C_weighting
import copy

def help_get_context():
    file_set_list = MicDataRecord.get_fileset()
    records = MicDataRecord.objects.all().order_by('pk')
    name_list = []
    for record in records:
        name_list.append(record.record_Name)
    return file_set_list, name_list, records

def spec_prop_abs_coeff_graphs():
    plt.switch_backend('AGG')
    return [graphs_snr_prop.prop_snr_pred_dist(dist_array_lin),
            graphs_snr_prop.get_avg_snr_vs_dist(dist_array_big),
            graphs_snr_prop.get_spec_prop_abs_coeff_hum(),
            graphs_snr_prop.get_spec_prop_abs_coeff_temp(),
            graphs_snr_prop.get_spec_prop_abs_coeff_dist(dist_array_lin),
            graphs_snr_prop.get_spec_prop_abs_coeff_dist(dist_array_log),
            graphs_snr_prop.get_spec_prop_abs_coeff_p(p_bar_array, p_ref),
            graphs_snr_prop.get_spec_prop_abs_coeff_p(p_bar_array, p_bar_array)]

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
    # context['signal_File'] = mic_Data_Record.filename()
    # context['reference_File'] = mic_Data_Record.filename()
    # start_dur_list = mic_Data_Record.get_start_dur()
    record_DB_dict = mic_Data_Record.__dict__
    record_DB_dict_fixed = copy.deepcopy(record_DB_dict)
    del record_DB_dict_fixed['record_Name'], record_DB_dict_fixed['description'], record_DB_dict_fixed['prediction_Harmonics']
    del record_DB_dict_fixed['_state'], record_DB_dict_fixed['id']
    file_list = []
    for attr, value in record_DB_dict_fixed.items():
        if mic_Data_Record.filename(attr):
            context[attr] = mic_Data_Record.filename(attr)
            file_list.append('./Uploads/Recordings/' + attr + '/' + context[attr])
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

def find_graph(graph_type, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record=None):
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
            context[graph_type] = graphs_temporal.get_signal(plot_me[0], plot_me[1], name, mic_Data_Record)
        case 'cepstrum_Graph':
            context[graph_type] = graphs_temporal.get_cepstrum(plot_me[0], plot_me[1], name, mic_Data_Record)
        case 'hilbert_Phase_Graph':
            context[graph_type] = graphs_temporal.get_inst_phase(plot_me[0], plot_me[1], name, mic_Data_Record)
        case 'onset_Strength_Graph':
            context[graph_type] = graphs_temporal.get_onset_strength(plot_me[0], name, mic_Data_Record)
        case 'lag_Autocorrelation_Graph':
            context[graph_type] = graphs_temporal.get_lag_autocorrelation(plot_me[0], name, mic_Data_Record)
        case 'BPM_Autocorrelation_Graph':
            context[graph_type] = graphs_temporal.get_bpm_autocorrelation(plot_me[0], name, mic_Data_Record)
        case 'autocorrelation_Tempogram':
            context[graph_type] = graphs_temporal.get_autocorr_tempogram(plot_me[0], name, mic_Data_Record)
        case 'fourier_Tempogram':
            context[graph_type] = graphs_temporal.get_fourier_tempogram(plot_me[0], name, mic_Data_Record)
        case 'average_PSD_Graph':
            context[graph_type] = graphs_spectral.get_PSD(plot_me[2], name, mic_Data_Record)
        case 'phase_Spectrum_Graph':
            context[graph_type] = graphs_spectral.get_phase_spectrum(plot_me[1], name, mic_Data_Record)
        case 'pure_Signal_SNR_Graph':
            if norm_sig and norm_noise:
                context[graph_type] = graphs_snr_prop.get_SNR(norm_sig[2], norm_noise[2], 'Given Signal and Noise', graph_type, name, mic_Data_Record)
            else:
                context[graph_type] = None
        case 'system_Signal_SNR_Graph':
            if true_sig and norm_noisy_sig:
                context[graph_type] = graphs_snr_prop.get_SNR(true_sig[2], norm_noisy_sig[2], 'System Approach', graph_type, name, mic_Data_Record)
            else:
                context[graph_type] = None
        case 'given_Signal_SNR_Graph':
            if norm_sig and norm_noisy_sig:
                context[graph_type] = graphs_snr_prop.get_SNR(norm_sig[2], norm_noisy_sig[2], 'Given Signal', graph_type, name, mic_Data_Record)
            else:
                context[graph_type] = None
        case 'given_Noise_SNR_Graph':
            if norm_noisy_sig and norm_noise:
                context[graph_type] = graphs_snr_prop.get_SNR(norm_noisy_sig[2], norm_noise[2], 'Given Noise', graph_type, name, mic_Data_Record)
            else:
                context[graph_type] = None
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
                context[graph_type] = graphs_snr_prop.get_avg_snr_vs_dist(dist_array_big, name, mic_Data_Record, db_rolled_avg, tunnel_dist)
        case 'spectrogram':
            context[graph_type] = graphs_spectral.get_spectrogram(plot_me[0], name, mic_Data_Record)
        case 'mellin_Spectrogram':
            context[graph_type] = graphs_spectral.get_mellin(plot_me[0], name, mic_Data_Record)
        case 'percussive_Spectrogram':
            context[graph_type] = graphs_spectral.get_percussive(plot_me[0], name, mic_Data_Record)
        case 'harmonic_Spectrogram':
            context[graph_type] = graphs_spectral.get_harmonic(plot_me[0], name, mic_Data_Record)
        case 'harmonic_Prediction_Graph':
            context[graph_type] = graphs_spectral.get_harmonic_prediction(plot_me[0], mic_Data_Record.prediction_Harmonics, name, mic_Data_Record)
    return context