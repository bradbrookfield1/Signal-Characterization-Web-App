from django.views import generic
from .models import MicDataRecord
from .graphic_interfacing import charts_preprocess
from . import graphs_temporal
from .views import help_get_context

class OriginalSignalListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/list_without_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = graphs_temporal.get_signal(norm_lib_list, norm_start_dur, norm_sig_list)
        return context
    
class CepstrumListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_without_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = graphs_temporal.get_cepstrum(norm_lib_list, norm_sig_list)
        context['type'] = 'Cepstrum'
        return context

class HilbertPhaseListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_without_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = graphs_temporal.get_inst_phase(norm_lib_list, norm_sig_list)
        context['type'] = 'Hilbert Phase'
        return context

class OnsetStrengthListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_without_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = graphs_temporal.get_onset_strength(norm_lib_list)
        context['type'] = 'Onset Strength'
        return context
    
class AutocorrelationLagListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/list_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = graphs_temporal.get_lag_autocorrelation(norm_lib_list)
        return context
    
class AutocorrelationBPMListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = graphs_temporal.get_bpm_autocorrelation(norm_lib_list)
        context['type'] = 'Autocorrelation (BPM)'
        return context
    
class AutocorrTempogramListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = graphs_temporal.get_autocorr_tempogram(norm_lib_list)
        context['type'] = 'Autocorrelation Tempogram'
        return context
    
class FourierTempogramListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = graphs_temporal.get_fourier_tempogram(norm_lib_list)
        context['type'] = 'Fourier Tempogram'
        return context