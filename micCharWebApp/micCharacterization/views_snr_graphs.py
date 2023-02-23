from django.views import generic
from .models import MicDataRecord
from .views_custom_functions import find_graph, list_intro
from .graphic_interfacing import file_path_to_img

class PureSNRListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('SNR')
        path_list = db_list.values_list('pure_Signal_SNR_Graph', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('pure_Signal_SNR_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.pure_Signal_SNR_Graph = context['pure_Signal_SNR_Graph']
                db.save()
                good_graph_list.append(file_path_to_img(context['pure_Signal_SNR_Graph']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'pure-SNR-list-refreshed'
        return context

class PureSNRRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('SNR')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('pure_Signal_SNR_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.pure_Signal_SNR_Graph = context['pure_Signal_SNR_Graph']
            db.save()
            good_graph_list.append(file_path_to_img(context['pure_Signal_SNR_Graph']))
        context['graphs'] = good_graph_list
        context['type'] = 'pure-SNR-list-refreshed'
        return context

class SystemSNRListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('SNR')
        path_list = db_list.values_list('system_Signal_SNR_Graph', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('system_Signal_SNR_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.system_Signal_SNR_Graph = context['system_Signal_SNR_Graph']
                db.save()
                good_graph_list.append(file_path_to_img(context['system_Signal_SNR_Graph']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'system-SNR-list-refreshed'
        return context

class SystemSNRRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('SNR')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('system_Signal_SNR_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.system_Signal_SNR_Graph = context['system_Signal_SNR_Graph']
            db.save()
            good_graph_list.append(file_path_to_img(context['system_Signal_SNR_Graph']))
        context['graphs'] = good_graph_list
        context['type'] = 'system-SNR-list-refreshed'
        return context

class SignalSNRListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('SNR')
        path_list = db_list.values_list('given_Signal_SNR_Graph', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('given_Signal_SNR_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.given_Signal_SNR_Graph = context['given_Signal_SNR_Graph']
                db.save()
                good_graph_list.append(file_path_to_img(context['given_Signal_SNR_Graph']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'signal-SNR-list-refreshed'
        return context

class SignalSNRRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('SNR')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('given_Signal_SNR_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.given_Signal_SNR_Graph = context['given_Signal_SNR_Graph']
            db.save()
            good_graph_list.append(file_path_to_img(context['given_Signal_SNR_Graph']))
        context['graphs'] = good_graph_list
        context['type'] = 'signal-SNR-list-refreshed'
        return context

class NoiseSNRListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('SNR')
        path_list = db_list.values_list('given_Noise_SNR_Graph', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('given_Noise_SNR_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.given_Noise_SNR_Graph = context['given_Noise_SNR_Graph']
                db.save()
                good_graph_list.append(file_path_to_img(context['given_Noise_SNR_Graph']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'noise-SNR-list-refreshed'
        return context

class NoiseSNRRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('SNR')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('given_Noise_SNR_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.given_Noise_SNR_Graph = context['given_Noise_SNR_Graph']
            db.save()
            good_graph_list.append(file_path_to_img(context['given_Noise_SNR_Graph']))
        context['graphs'] = good_graph_list
        context['type'] = 'noise-SNR-list-refreshed'
        return context

class AvgSNRDistanceListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('SNR')
        path_list = db_list.values_list('average_SNR_Distance_Graph', flat=True)
        good_graph_list = []
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('average_SNR_Distance_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.average_SNR_Distance_Graph = context['average_SNR_Distance_Graph']
                db.save()
                good_graph_list.append(file_path_to_img(context['average_SNR_Distance_Graph']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'avg-SNR-dist-list-refreshed'
        return context

class AvgSNRDistanceRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/more_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('SNR')
        good_graph_list = []
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('average_SNR_Distance_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.average_SNR_Distance_Graph = context['average_SNR_Distance_Graph']
            db.save()
            good_graph_list.append(file_path_to_img(context['average_SNR_Distance_Graph']))
        context['graphs'] = good_graph_list
        context['type'] = 'avg-SNR-dist-list-refreshed'
        return context