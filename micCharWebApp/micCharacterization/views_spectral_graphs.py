from django.views import generic
from .models import MicDataRecord
from .views_custom_functions import find_graph, list_intro
from .graphic_interfacing import file_path_to_img

class PowerSpectralDensityListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Spectral')
        path_list = db_list.values_list('average_PSD_Graph', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('average_PSD_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.average_PSD_Graph = context['average_PSD_Graph']
                db.save()
                good_graph_list.append(file_path_to_img(context['average_PSD_Graph']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'power-spectral-density-list-refreshed'
        return context

class PowerSpectralDensityRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Spectral')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('average_PSD_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.average_PSD_Graph = context['average_PSD_Graph']
            db.save()
            good_graph_list.append(file_path_to_img(context['average_PSD_Graph']))
        context['graphs'] = good_graph_list
        context['type'] = 'power-spectral-density-list-refreshed'
        return context

class PhaseSpectrumListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Spectral')
        path_list = db_list.values_list('phase_Spectrum_Graph', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('phase_Spectrum_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.phase_Spectrum_Graph = context['phase_Spectrum_Graph']
                db.save()
                good_graph_list.append(file_path_to_img(context['phase_Spectrum_Graph']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'phase-spectrum-list-refreshed'
        return context

class PhaseSpectrumRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Spectral')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('phase_Spectrum_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.phase_Spectrum_Graph = context['phase_Spectrum_Graph']
            db.save()
            good_graph_list.append(file_path_to_img(context['phase_Spectrum_Graph']))
        context['graphs'] = good_graph_list
        context['type'] = 'phase-spectrum-list-refreshed'
        return context

class SpectrogramListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Spectral')
        path_list = db_list.values_list('spectrogram', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('spectrogram', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.spectrogram = context['spectrogram']
                db.save()
                good_graph_list.append(file_path_to_img(context['spectrogram']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'spectrogram-list-refreshed'
        return context

class SpectrogramRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Spectral')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('spectrogram', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.spectrogram = context['spectrogram']
            db.save()
            good_graph_list.append(file_path_to_img(context['spectrogram']))
        context['graphs'] = good_graph_list
        context['type'] = 'spectrogram-list-refreshed'
        return context

class MellinListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Spectral')
        path_list = db_list.values_list('mellin_Spectrogram', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('mellin_Spectrogram', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.mellin_Spectrogram = context['mellin_Spectrogram']
                db.save()
                good_graph_list.append(file_path_to_img(context['mellin_Spectrogram']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'mellin-spectrogram-list-refreshed'
        return context

class MellinRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Spectral')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('mellin_Spectrogram', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.mellin_Spectrogram = context['mellin_Spectrogram']
            db.save()
            good_graph_list.append(file_path_to_img(context['mellin_Spectrogram']))
        context['graphs'] = good_graph_list
        context['type'] = 'mellin-spectrogram-list-refreshed'
        return context

class PercussiveComponentsListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Spectral')
        path_list = db_list.values_list('percussive_Spectrogram', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('percussive_Spectrogram', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.percussive_Spectrogram = context['percussive_Spectrogram']
                db.save()
                good_graph_list.append(file_path_to_img(context['percussive_Spectrogram']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'percussive-components-list-refreshed'
        return context

class PercussiveComponentsRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Spectral')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('percussive_Spectrogram', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.percussive_Spectrogram = context['percussive_Spectrogram']
            db.save()
            good_graph_list.append(file_path_to_img(context['percussive_Spectrogram']))
        context['graphs'] = good_graph_list
        context['type'] = 'percussive-components-list-refreshed'
        return context

class HarmonicComponentsListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Spectral')
        path_list = db_list.values_list('harmonic_Spectrogram', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('harmonic_Spectrogram', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.harmonic_Spectrogram = context['harmonic_Spectrogram']
                db.save()
                good_graph_list.append(file_path_to_img(context['harmonic_Spectrogram']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'harmonic-components-list-refreshed'
        return context

class HarmonicComponentsRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Spectral')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('harmonic_Spectrogram', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.harmonic_Spectrogram = context['harmonic_Spectrogram']
            db.save()
            good_graph_list.append(file_path_to_img(context['harmonic_Spectrogram']))
        context['graphs'] = good_graph_list
        context['type'] = 'harmonic-components-list-refreshed'
        return context

class HarmonicPredictionListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Spectral')
        path_list = db_list.values_list('harmonic_Prediction_Graph', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('harmonic_Prediction_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec, None, records)
                db.harmonic_Prediction_Graph = context['harmonic_Prediction_Graph']
                db.save()
                good_graph_list.append(file_path_to_img(context['harmonic_Prediction_Graph']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'harmonic-prediction-list-refreshed'
        return context

class HarmonicPredictionRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Spectral')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('harmonic_Prediction_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec, None, records)
            db.harmonic_Prediction_Graph = context['harmonic_Prediction_Graph']
            db.save()
            good_graph_list.append(file_path_to_img(context['harmonic_Prediction_Graph']))
        context['graphs'] = good_graph_list
        context['type'] = 'harmonic-prediction-list-refreshed'
        return context