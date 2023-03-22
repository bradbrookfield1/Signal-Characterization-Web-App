from django.views import generic
from micCharacterization.models import MicDataRecord
from micCharacterization.views_functions import find_graph, list_intro, help_get_context, detail_intro
from micCharacterization.graphic_interfacing import file_path_to_img
from .models import TemporalDatabase

class TemporalListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/temporaldatabase_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(TemporalListView, self).get_context_data(**kwargs)
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

class TemporalDetailView(generic.DetailView):
    model = TemporalDatabase
    
    def get_context_data(self, **kwargs):
        context = super(TemporalDetailView, self).get_context_data(**kwargs)
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
        
        for attr, value in temp_DB_dict.items():
            if value == None:
                context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                setattr(temp_DB, attr, context[attr])
                context[attr] = file_path_to_img(context[attr])
            else:
                context[attr] = eval('file_path_to_img(temp_DB.' + attr + ')')
        temp_DB.save()
        context['type'] = 'temporal:detail'
        context['object'] = mic_Data_Record
        return context

class TemporalRefreshedDetailView(generic.DetailView):
    model = TemporalDatabase
    
    def get_context_data(self, **kwargs):
        context = super(TemporalRefreshedDetailView, self).get_context_data(**kwargs)
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
        
        for attr, value in temp_DB_dict.items():
            context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
            setattr(temp_DB, attr, context[attr])
            context[attr] = file_path_to_img(context[attr])
        temp_DB.save()
        context['type'] = 'temporal:detail-refreshed'
        context['object'] = mic_Data_Record
        return context

class OriginalSignalListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/list_without_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        path_list = db_list.values_list('signal_Graph', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('signal_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.signal_Graph = context['signal_Graph']
                db.save()
                good_graph_list.append(file_path_to_img(context['signal_Graph']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:original-signal-list-refreshed'
        return context

class OriginalSignalRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/list_without_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('signal_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.signal_Graph = context['signal_Graph']
            db.save()
            good_graph_list.append(file_path_to_img(context['signal_Graph']))
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:original-signal-list-refreshed'
        return context

class CepstrumListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/more_without_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        path_list = db_list.values_list('cepstrum_Graph', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('cepstrum_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.cepstrum_Graph = context['cepstrum_Graph']
                db.save()
                good_graph_list.append(file_path_to_img(context['cepstrum_Graph']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:cepstrum-list-refreshed'
        return context
    
class CepstrumRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/more_without_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('cepstrum_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.cepstrum_Graph = context['cepstrum_Graph']
            db.save()
            good_graph_list.append(file_path_to_img(context['cepstrum_Graph']))
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:cepstrum-list-refreshed'
        return context

class HilbertPhaseListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/more_without_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        path_list = db_list.values_list('hilbert_Phase_Graph', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('hilbert_Phase_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.hilbert_Phase_Graph = context['hilbert_Phase_Graph']
                db.save()
                good_graph_list.append(file_path_to_img(context['hilbert_Phase_Graph']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:hilbert-phase-list-refreshed'
        return context

class HilbertPhaseRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/more_without_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('hilbert_Phase_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.hilbert_Phase_Graph = context['hilbert_Phase_Graph']
            db.save()
            good_graph_list.append(file_path_to_img(context['hilbert_Phase_Graph']))
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:hilbert-phase-list-refreshed'
        return context

class OnsetStrengthListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/more_without_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        path_list = db_list.values_list('onset_Strength_Graph', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('onset_Strength_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.onset_Strength_Graph = context['onset_Strength_Graph']
                db.save()
                good_graph_list.append(file_path_to_img(context['onset_Strength_Graph']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:onset-strength-list-refreshed'
        return context
    
class OnsetStrengthRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/more_without_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('onset_Strength_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.onset_Strength_Graph = context['onset_Strength_Graph']
            db.save()
            good_graph_list.append(file_path_to_img(context['onset_Strength_Graph']))
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:onset-strength-list-refreshed'
        return context
    
class AutocorrelationLagListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/list_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        path_list = db_list.values_list('lag_Autocorrelation_Graph', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('lag_Autocorrelation_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.lag_Autocorrelation_Graph = context['lag_Autocorrelation_Graph']
                db.save()
                good_graph_list.append(file_path_to_img(context['lag_Autocorrelation_Graph']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:autocorrelation-lag-list-refreshed'
        return context

class AutocorrelationLagRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/list_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('lag_Autocorrelation_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.lag_Autocorrelation_Graph = context['lag_Autocorrelation_Graph']
            db.save()
            good_graph_list.append(file_path_to_img(context['lag_Autocorrelation_Graph']))
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:autocorrelation-lag-list-refreshed'
        return context
    
class AutocorrelationBPMListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        path_list = db_list.values_list('BPM_Autocorrelation_Graph', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('BPM_Autocorrelation_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.BPM_Autocorrelation_Graph = context['BPM_Autocorrelation_Graph']
                db.save()
                good_graph_list.append(file_path_to_img(context['BPM_Autocorrelation_Graph']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:autocorrelation-bpm-list-refreshed'
        return context

class AutocorrelationBPMRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('BPM_Autocorrelation_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.BPM_Autocorrelation_Graph = context['BPM_Autocorrelation_Graph']
            db.save()
            good_graph_list.append(context['BPM_Autocorrelation_Graph'])
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:autocorrelation-bpm-list-refreshed'
        return context
    
class AutocorrTempogramListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        path_list = db_list.values_list('autocorrelation_Tempogram', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('autocorrelation_Tempogram', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.autocorrelation_Tempogram = context['autocorrelation_Tempogram']
                db.save()
                good_graph_list.append(file_path_to_img(context['autocorrelation_Tempogram']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:autocorrelation-tempogram-list-refreshed'
        return context

class AutocorrTempogramRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('autocorrelation_Tempogram', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.autocorrelation_Tempogram = context['autocorrelation_Tempogram']
            db.save()
            good_graph_list.append(file_path_to_img(context['autocorrelation_Tempogram']))
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:autocorrelation-tempogram-list-refreshed'
        return context
    
class FourierTempogramListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        path_list = db_list.values_list('fourier_Tempogram', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('fourier_Tempogram', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.fourier_Tempogram = context['fourier_Tempogram']
                db.save()
                good_graph_list.append(file_path_to_img(context['fourier_Tempogram']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:fourier-tempogram-list-refreshed'
        return context

class FourierTempogramRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'temporalDatabase/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Temporal')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('fourier_Tempogram', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.fourier_Tempogram = context['fourier_Tempogram']
            db.save()
            good_graph_list.append(file_path_to_img(context['fourier_Tempogram']))
        context['graphs'] = good_graph_list
        context['type'] = 'temporal:fourier-tempogram-list-refreshed'
        return context