from django.views import generic
from .models import MicDataRecord
from .graphic_interfacing import charts_preprocess
from . import graphs_spectral
from .views import help_get_context

class PowerSpectralDensityListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = graphs_spectral.get_PSD(norm_lib_list)
        context['type'] = 'Power Spectral Density'
        return context

class PhaseSpectrumListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = graphs_spectral.get_phase_spectrum(norm_sig_list)
        context['type'] = 'Phase Spectrum'
        return context

class HarmonicPredictionListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        records = MicDataRecord.get_all_records()
        pred_harm = []
        for rec in records:
            pred_harm.append(rec.prediction_Harmonics)
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = graphs_spectral.get_harmonic_prediction(norm_lib_list, pred_harm)[0]
        context['type'] = 'Harmonic Prediction'
        return context

class PowerSpectrumListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = graphs_spectral.get_PS(norm_lib_list)
        context['type'] = 'Power Spectrum'
        return context

class MellinListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = graphs_spectral.get_mellin(norm_lib_list)
        context['type'] = 'Mellin Spectrum'
        return context

class PercussiveComponentsListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = graphs_spectral.get_percussive(norm_lib_list)
        context['type'] = 'Percussive Components'
        return context

class HarmonicComponentsListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = graphs_spectral.get_harmonic(norm_lib_list)
        context['type'] = 'Harmonic Components'
        return context