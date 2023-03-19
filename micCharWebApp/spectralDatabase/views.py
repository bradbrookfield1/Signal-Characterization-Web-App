from django.views import generic
from micCharacterization.models import MicDataRecord
from micCharacterization.views_functions import find_graph, list_intro, help_get_context, detail_intro, get_hpss_audio
from micCharacterization.graphic_interfacing import file_path_to_img
from .models import SpectralDatabase

class SpectralListView(generic.ListView):
    model = MicDataRecord
    template_name = 'spectralDatabase/spectraldatabase_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(SpectralListView, self).get_context_data(**kwargs)
        file_set_list, name_list, records = help_get_context()
        file_list = []
        for rec in records:
            if rec.noisy_Signal_File:
                file = rec.noisy_Signal_File
            elif rec.measured_Signal_File:
                file = rec.measured_Signal_File
            elif rec.noise_File:
                file = rec.noise_File
            else:
                file = rec.true_Signal_File
            file_list.append(file)
        context['file_list'] = file_list
        context['length'] = [i for i in range(len(file_list))]
        context['records'] = records
        return context

class SpectralDetailView(generic.DetailView):
    model = SpectralDatabase
    
    def get_context_data(self, **kwargs):
        context = super(SpectralDetailView, self).get_context_data(**kwargs)
        mic_Data_Record = self.get_object().mic_Data_Record
        name = str(mic_Data_Record)
        context, norm_noisy_sig, norm_sig, norm_noise, true_sig, temp_DB_dict, spec_DB_dict, snr_DB_dict, stat_DB_dict, temp_DB, spec_DB, snr_DB, stat_DB = detail_intro(context, mic_Data_Record)
        
        if norm_noisy_sig:
            context['noisy_Signal_Harmonics'] = mic_Data_Record.noisy_Signal_Harmonics
            context['noisy_Signal_Percussives'] = mic_Data_Record.noisy_Signal_Percussives
        if norm_sig:
            context['measured_Signal_Harmonics'] = mic_Data_Record.measured_Signal_Harmonics
            context['measured_Signal_Percussives'] = mic_Data_Record.measured_Signal_Percussives
        if norm_noise:
            context['noise_Harmonics'] = mic_Data_Record.noise_Harmonics
            context['noise_Percussives'] = mic_Data_Record.noise_Percussives
        if true_sig:
            context['true_Signal_Harmonics'] = mic_Data_Record.true_Signal_Harmonics
            context['true_Signal_Percussives'] = mic_Data_Record.true_Signal_Percussives
        
        for attr, value in spec_DB_dict.items():
            if value == None:
                context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                setattr(spec_DB, attr, context[attr])
                context[attr] = file_path_to_img(context[attr])
            else:
                context[attr] = eval('file_path_to_img(spec_DB.' + attr + ')')
        spec_DB.save()
        context['type'] = 'spectral:detail'
        context['object'] = mic_Data_Record
        
        return context

class SpectralRefreshedDetailView(generic.DetailView):
    model = SpectralDatabase
    
    def get_context_data(self, **kwargs):
        context = super(SpectralRefreshedDetailView, self).get_context_data(**kwargs)
        mic_Data_Record = self.get_object().mic_Data_Record
        name = str(mic_Data_Record)
        context, norm_noisy_sig, norm_sig, norm_noise, true_sig, temp_DB_dict, spec_DB_dict, snr_DB_dict, stat_DB_dict, temp_DB, spec_DB, snr_DB, stat_DB = detail_intro(context, mic_Data_Record)
        
        if norm_noisy_sig:
            context['noisy_Signal_Harmonics'] = mic_Data_Record.noisy_Signal_Harmonics
            context['noisy_Signal_Percussives'] = mic_Data_Record.noisy_Signal_Percussives
        if norm_sig:
            context['measured_Signal_Harmonics'] = mic_Data_Record.measured_Signal_Harmonics
            context['measured_Signal_Percussives'] = mic_Data_Record.measured_Signal_Percussives
        if norm_noise:
            context['noise_Harmonics'] = mic_Data_Record.noise_Harmonics
            context['noise_Percussives'] = mic_Data_Record.noise_Percussives
        if true_sig:
            context['true_Signal_Harmonics'] = mic_Data_Record.true_Signal_Harmonics
            context['true_Signal_Percussives'] = mic_Data_Record.true_Signal_Percussives
        
        for attr, value in spec_DB_dict.items():
            context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
            setattr(spec_DB, attr, context[attr])
            context[attr] = file_path_to_img(context[attr])
        spec_DB.save()
        context['type'] = 'spectral:detail-refreshed'
        context['object'] = mic_Data_Record
        return context

class PowerSpectralDensityListView(generic.ListView):
    model = MicDataRecord
    template_name = 'spectralDatabase/list_with_sidebar.html'
    
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
        context['type'] = 'spectral:power-spectral-density-list-refreshed'
        return context

class PowerSpectralDensityRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'spectralDatabase/list_with_sidebar.html'
    
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
        context['type'] = 'spectral:power-spectral-density-list-refreshed'
        return context

class PhaseSpectrumListView(generic.ListView):
    model = MicDataRecord
    template_name = 'spectralDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'spectral:phase-spectrum-list-refreshed'
        return context

class PhaseSpectrumRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'spectralDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'spectral:phase-spectrum-list-refreshed'
        return context

class SpectrogramListView(generic.ListView):
    model = MicDataRecord
    template_name = 'spectralDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'spectral:spectrogram-list-refreshed'
        return context

class SpectrogramRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'spectralDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'spectral:spectrogram-list-refreshed'
        return context

class MellinListView(generic.ListView):
    model = MicDataRecord
    template_name = 'spectralDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'spectral:mellin-spectrogram-list-refreshed'
        return context

class MellinRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'spectralDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'spectral:mellin-spectrogram-list-refreshed'
        return context

class PercussiveComponentsListView(generic.ListView):
    model = MicDataRecord
    template_name = 'spectralDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'spectral:percussive-components-list-refreshed'
        return context

class PercussiveComponentsRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'spectralDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'spectral:percussive-components-list-refreshed'
        return context

class HarmonicComponentsListView(generic.ListView):
    model = MicDataRecord
    template_name = 'spectralDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'spectral:harmonic-components-list-refreshed'
        return context

class HarmonicComponentsRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'spectralDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'spectral:harmonic-components-list-refreshed'
        return context

class HarmonicPredictionListView(generic.ListView):
    model = MicDataRecord
    template_name = 'spectralDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'spectral:harmonic-prediction-list-refreshed'
        return context

class HarmonicPredictionRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'spectralDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'spectral:harmonic-prediction-list-refreshed'
        return context