from .models import MicDataRecord, TemporalDatabase, SpectralDatabase
from .graphic_interfacing import charts_preprocess
from . import graphs_temporal, graphs_spectral

def help_get_context():
    file_set_list = MicDataRecord.get_fileset()
    records = MicDataRecord.objects.all().order_by('pk')
    file_set = []
    start_dur_list = []
    name_list = []
    i = range(len(records))
    for idx, f in zip(i, file_set_list):
        file_set.append('./Uploads/Recordings/' + f)
        start_dur_list.append(records[idx].get_start_dur())
        name_list.append(records[idx].record_Name)
    return file_set, start_dur_list, name_list, records

def list_intro():
    file_set, start_dur_list, name_list, records = help_get_context()
    norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
    temp_DBs = TemporalDatabase.objects.all().order_by('pk')
    spec_DBs = SpectralDatabase.objects.all().order_by('pk')
    return norm_lib_list, norm_start_dur, norm_sig_list, name_list, records, temp_DBs, spec_DBs

def detail_intro(context, mic_Data_Record):
    context['signal_File'] = mic_Data_Record.sig_filename()
    context['reference_File'] = mic_Data_Record.ref_filename()
    start_dur_list = mic_Data_Record.get_start_dur()
    norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(['./Uploads/Recordings/' + context['signal_File']], [start_dur_list])
    temp_DB = TemporalDatabase.objects.filter(mic_Data_Record=mic_Data_Record).get()
    spec_DB = SpectralDatabase.objects.filter(mic_Data_Record=mic_Data_Record).get()
    temp_DB_dict = temp_DB.__dict__
    spec_DB_dict = spec_DB.__dict__
    del spec_DB_dict['harmonic_Prediction_Graph']
    return context, norm_lib_list, norm_start_dur, norm_sig_list, temp_DB_dict, spec_DB_dict, temp_DB, spec_DB

def delete_intro(mic_Data_Record):
    temp_DB = TemporalDatabase.objects.filter(mic_Data_Record=mic_Data_Record).get()
    spec_DB = SpectralDatabase.objects.filter(mic_Data_Record=mic_Data_Record).get()
    temp_DB_dict_fixed = temp_DB.__dict__
    spec_DB_dict_fixed = spec_DB.__dict__
    del spec_DB_dict_fixed['harmonic_Prediction_Graph']
    del temp_DB_dict_fixed['_state'], temp_DB_dict_fixed['id'], temp_DB_dict_fixed['mic_Data_Record_id']
    del spec_DB_dict_fixed['_state'], spec_DB_dict_fixed['id'], spec_DB_dict_fixed['mic_Data_Record_id']
    return temp_DB_dict_fixed, spec_DB_dict_fixed

def find_graph(graph_type, context, name, norm_lib_list, norm_start_dur, norm_sig_list, mic_Data_Record=None):
    match graph_type:
        case 'signal_Graph':
            context['signal_Graph'] = graphs_temporal.get_signal(norm_lib_list, norm_start_dur, norm_sig_list, name, mic_Data_Record)
        case 'cepstrum_Graph':
            context['cepstrum_Graph'] = graphs_temporal.get_cepstrum(norm_lib_list, norm_sig_list, name, mic_Data_Record)
        case 'hilbert_Phase_Graph':
            context['hilbert_Phase_Graph'] = graphs_temporal.get_inst_phase(norm_lib_list, norm_sig_list, name, mic_Data_Record)
        case 'onset_Strength_Graph':
            context['onset_Strength_Graph'] = graphs_temporal.get_onset_strength(norm_lib_list, name, mic_Data_Record)
        case 'lag_Autocorrelation_Graph':
            context['lag_Autocorrelation_Graph'] = graphs_temporal.get_lag_autocorrelation(norm_lib_list, name, mic_Data_Record)
        case 'BPM_Autocorrelation_Graph':
            context['BPM_Autocorrelation_Graph'] = graphs_temporal.get_bpm_autocorrelation(norm_lib_list, name, mic_Data_Record)
        case 'autocorrelation_Tempogram':
            context['autocorrelation_Tempogram'] = graphs_temporal.get_autocorr_tempogram(norm_lib_list, name, mic_Data_Record)
        case 'fourier_Tempogram':
            context['fourier_Tempogram'] = graphs_temporal.get_fourier_tempogram(norm_lib_list, name, mic_Data_Record)
        case 'average_PSD_Graph':
            context['average_PSD_Graph'] = graphs_spectral.get_PSD(norm_lib_list, name, mic_Data_Record)
        case 'phase_Spectrum_Graph':
            context['phase_Spectrum_Graph'] = graphs_spectral.get_phase_spectrum(norm_sig_list, name, mic_Data_Record)
        case 'spectrogram':
            context['spectrogram'] = graphs_spectral.get_PS(norm_lib_list, name, mic_Data_Record)
        case 'mellin_Spectrogram':
            context['mellin_Spectrogram'] = graphs_spectral.get_mellin(norm_lib_list, name, mic_Data_Record)
        case 'percussive_Spectrogram':
            context['percussive_Spectrogram'] = graphs_spectral.get_percussive(norm_lib_list, name, mic_Data_Record)
        case 'harmonic_Spectrogram':
            context['harmonic_Spectrogram'] = graphs_spectral.get_harmonic(norm_lib_list, name, mic_Data_Record)
        case 'harmonic_Prediction_Graph':
            context['harmonic_Prediction_Graph'] = graphs_spectral.get_harmonic_prediction(norm_lib_list, mic_Data_Record.prediction_Harmonics, name, mic_Data_Record)
    return context