from .models import MicDataRecord, TemporalDatabase, SpectralDatabase
from .graphic_interfacing import charts_preprocess
from .calculations import calc_coeff
from . import graphs_temporal, graphs_spectral, graphs_other
from matplotlib import pyplot as plt
import numpy as np
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
    freqs = np.logspace(1, 4, 100)                          # Hz
    p_bar = 101425                                          # Pascals
    p_ref = 101325                                          # Pascals
    relative_humidity = 0.5                                 # Decimal
    temperature = 20                                        # Celcius
    distance = 1                                            # Meters
    
    rel_hum_array = [i/10 for i in range(11)]               # Decimal (0, 0.1, 0.2, ..., 1)
    temp_array = [((i*5 - 20) + 273.15) for i in range(9)]  # Kelvin (-20, -15, -10, ..., 20 deg C)
    dist_array_lin = np.linspace(1, 100, 10)                # Meters
    dist_array_log = np.logspace(0, 2, 10)
    p_bar_array = np.linspace(101325, 151325, 11)
    
    temperature = temperature + 273.15                      # To Kelvin
    freqs = freqs/(p_bar/101325)                            # Normalized by barometric pressure
    
    return [graphs_other.get_spec_prop_abs_coeff_hum(freqs, distance, temperature, rel_hum_array, p_bar, p_ref),
            graphs_other.get_spec_prop_abs_coeff_temp(freqs, distance, temp_array, relative_humidity, p_bar, p_ref),
            graphs_other.get_spec_prop_abs_coeff_dist(freqs, dist_array_lin, temperature, relative_humidity, p_bar, p_ref),
            graphs_other.get_spec_prop_abs_coeff_dist(freqs, dist_array_log, temperature, relative_humidity, p_bar, p_ref),
            graphs_other.get_spec_prop_abs_coeff_p(freqs, distance, temperature, relative_humidity, p_bar_array, p_ref),
            graphs_other.get_spec_prop_abs_coeff_p(freqs, distance, temperature, relative_humidity, p_bar_array, p_bar_array)]

def list_intro():
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
    temp_DBs = TemporalDatabase.objects.all().order_by('pk')
    spec_DBs = SpectralDatabase.objects.all().order_by('pk')
    return norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, temp_DBs, spec_DBs

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
    temp_DB_dict = temp_DB.__dict__
    spec_DB_dict = spec_DB.__dict__
    temp_DB_dict_fixed = copy.deepcopy(temp_DB_dict)
    spec_DB_dict_fixed = copy.deepcopy(spec_DB_dict)
    del temp_DB_dict_fixed['_state'], temp_DB_dict_fixed['id'], temp_DB_dict_fixed['mic_Data_Record_id']
    del spec_DB_dict_fixed['_state'], spec_DB_dict_fixed['id'], spec_DB_dict_fixed['mic_Data_Record_id']
    del spec_DB_dict_fixed['harmonic_Prediction_Graph']
    return context, norm_noisy_sig, norm_sig, norm_noise, true_sig, temp_DB_dict_fixed, spec_DB_dict_fixed, temp_DB, spec_DB

def delete_intro(mic_Data_Record):
    temp_DB = TemporalDatabase.objects.filter(mic_Data_Record=mic_Data_Record).get()
    spec_DB = SpectralDatabase.objects.filter(mic_Data_Record=mic_Data_Record).get()
    temp_DB_dict_fixed = temp_DB.__dict__
    spec_DB_dict_fixed = spec_DB.__dict__
    del spec_DB_dict_fixed['harmonic_Prediction_Graph']
    del temp_DB_dict_fixed['_state'], temp_DB_dict_fixed['id'], temp_DB_dict_fixed['mic_Data_Record_id']
    del spec_DB_dict_fixed['_state'], spec_DB_dict_fixed['id'], spec_DB_dict_fixed['mic_Data_Record_id']
    return temp_DB_dict_fixed, spec_DB_dict_fixed

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
            context['signal_Graph'] = graphs_temporal.get_signal(plot_me[0], plot_me[1], name, mic_Data_Record)
        case 'cepstrum_Graph':
            context['cepstrum_Graph'] = graphs_temporal.get_cepstrum(plot_me[0], plot_me[1], name, mic_Data_Record)
        case 'hilbert_Phase_Graph':
            context['hilbert_Phase_Graph'] = graphs_temporal.get_inst_phase(plot_me[0], plot_me[1], name, mic_Data_Record)
        case 'onset_Strength_Graph':
            context['onset_Strength_Graph'] = graphs_temporal.get_onset_strength(plot_me[0], name, mic_Data_Record)
        case 'lag_Autocorrelation_Graph':
            context['lag_Autocorrelation_Graph'] = graphs_temporal.get_lag_autocorrelation(plot_me[0], name, mic_Data_Record)
        case 'BPM_Autocorrelation_Graph':
            context['BPM_Autocorrelation_Graph'] = graphs_temporal.get_bpm_autocorrelation(plot_me[0], name, mic_Data_Record)
        case 'autocorrelation_Tempogram':
            context['autocorrelation_Tempogram'] = graphs_temporal.get_autocorr_tempogram(plot_me[0], name, mic_Data_Record)
        case 'fourier_Tempogram':
            context['fourier_Tempogram'] = graphs_temporal.get_fourier_tempogram(plot_me[0], name, mic_Data_Record)
        case 'average_PSD_Graph':
            context['average_PSD_Graph'] = graphs_spectral.get_PSD(plot_me[0], name, mic_Data_Record)
        case 'phase_Spectrum_Graph':
            context['phase_Spectrum_Graph'] = graphs_spectral.get_phase_spectrum(plot_me[1], name, mic_Data_Record)
        case 'pure_Signal_SNR_Graph':
            if norm_sig and norm_noise:
                context['pure_Signal_SNR_Graph'] = graphs_other.get_pure_SNR(norm_sig[0], norm_noise[0], name, mic_Data_Record)
            else:
                context['pure_Signal_SNR_Graph'] = None
        case 'system_Signal_SNR_Graph':
            if norm_noisy_sig and true_sig:
                context['system_Signal_SNR_Graph'] = graphs_other.get_SNR_system(norm_noisy_sig[0], true_sig[0], name, mic_Data_Record)
            else:
                context['system_Signal_SNR_Graph'] = None
        case 'given_Signal_SNR_Graph':
            if norm_noisy_sig and norm_sig:
                context['given_Signal_SNR_Graph'] = graphs_other.get_SNR_gvn_sig(norm_noisy_sig[0], norm_sig[0], name, mic_Data_Record)
            else:
                context['given_Signal_SNR_Graph'] = None
        case 'given_Noise_SNR_Graph':
            if norm_noisy_sig and norm_noise:
                context['given_Noise_SNR_Graph'] = graphs_other.get_SNR_gvn_noise(norm_noisy_sig[0], norm_noise[0], name, mic_Data_Record)
            else:
                context['given_Noise_SNR_Graph'] = None
        case 'spectrogram':
            context['spectrogram'] = graphs_spectral.get_spectrogram(plot_me[0], name, mic_Data_Record)
        case 'mellin_Spectrogram':
            context['mellin_Spectrogram'] = graphs_spectral.get_mellin(plot_me[0], name, mic_Data_Record)
        case 'percussive_Spectrogram':
            context['percussive_Spectrogram'] = graphs_spectral.get_percussive(plot_me[0], name, mic_Data_Record)
        case 'harmonic_Spectrogram':
            context['harmonic_Spectrogram'] = graphs_spectral.get_harmonic(plot_me[0], name, mic_Data_Record)
        case 'harmonic_Prediction_Graph':
            context['harmonic_Prediction_Graph'] = graphs_spectral.get_harmonic_prediction(plot_me[0], mic_Data_Record.prediction_Harmonics, name, mic_Data_Record)
    return context