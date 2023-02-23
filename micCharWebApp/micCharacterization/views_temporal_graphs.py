from django.views import generic
from .models import MicDataRecord
from .views_custom_functions import find_graph, list_intro
from .graphic_interfacing import file_path_to_img

class OriginalSignalListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/list_without_sidebar.html'
    
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
        context['type'] = 'original-signal-list-refreshed'
        return context

class OriginalSignalRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/list_without_sidebar.html'
    
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
        context['type'] = 'original-signal-list-refreshed'
        return context

class CepstrumListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_without_sidebar.html'
    
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
        context['type'] = 'cepstrum-list-refreshed'
        return context
    
class CepstrumRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_without_sidebar.html'
    
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
        context['type'] = 'cepstrum-list-refreshed'
        return context

class HilbertPhaseListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_without_sidebar.html'
    
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
        context['type'] = 'hilbert-phase-list-refreshed'
        return context

class HilbertPhaseRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_without_sidebar.html'
    
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
        context['type'] = 'hilbert-phase-list-refreshed'
        return context

class OnsetStrengthListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_without_sidebar.html'
    
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
        context['type'] = 'onset-strength-list-refreshed'
        return context
    
class OnsetStrengthRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_without_sidebar.html'
    
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
        context['type'] = 'onset-strength-list-refreshed'
        return context
    
class AutocorrelationLagListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/list_with_sidebar.html'
    
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
        context['type'] = 'autocorrelation-lag-list-refreshed'
        return context

class AutocorrelationLagRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/list_with_sidebar.html'
    
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
        context['type'] = 'autocorrelation-lag-list-refreshed'
        return context
    
class AutocorrelationBPMListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
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
        context['type'] = 'autocorrelation-bpm-list-refreshed'
        return context

class AutocorrelationBPMRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
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
        context['type'] = 'autocorrelation-bpm-list-refreshed'
        return context
    
class AutocorrTempogramListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
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
        context['type'] = 'autocorrelation-tempogram-list-refreshed'
        return context

class AutocorrTempogramRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
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
        context['type'] = 'autocorrelation-tempogram-list-refreshed'
        return context
    
class FourierTempogramListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
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
        context['type'] = 'fourier-tempogram-list-refreshed'
        return context

class FourierTempogramRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
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
        context['type'] = 'fourier-tempogram-list-refreshed'
        return context