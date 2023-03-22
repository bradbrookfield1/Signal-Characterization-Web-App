from django.views import generic
from micCharacterization.models import MicDataRecord
from micCharacterization.views_functions import find_graph, list_intro, help_get_context, detail_intro
from micCharacterization.graphic_interfacing import file_path_to_img
from .models import SNRDatabase

class SNRListView(generic.ListView):
    model = MicDataRecord
    template_name = 'snrDatabase/snrdatabase_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(SNRListView, self).get_context_data(**kwargs)
        file_set_list, name_list, records = help_get_context()
        file_list = []
        has_items_list = []
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
            db = SNRDatabase.objects.filter(mic_Data_Record=rec).get()
            has_items = False if not (rec.measured_Signal_File and rec.noise_File or rec.noisy_Signal_File and rec.measured_Signal_File or rec.noisy_Signal_File and rec.noise_File or rec.noisy_Signal_File and rec.true_Signal_File) else True
            has_items_list.append(has_items)
        context['good_list'] = zip(context['object_list'], has_items_list)
        context['file_list'] = file_list
        context['length'] = [i for i in range(len(file_list))]
        context['records'] = records
        return context

class SNRDetailView(generic.DetailView):
    model = SNRDatabase
    
    def get_context_data(self, **kwargs):
        context = super(SNRDetailView, self).get_context_data(**kwargs)
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
        
        for attr, value in snr_DB_dict.items():
            if value == None:
                if attr == 'pure_Signal_SNR_Graph':
                    if norm_sig and norm_noise:
                        context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                        setattr(snr_DB, attr, context[attr])
                        context[attr] = file_path_to_img(context[attr])
                elif attr == 'system_Signal_SNR_Graph':
                    if norm_noisy_sig and true_sig:
                        context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                        setattr(snr_DB, attr, context[attr])
                        context[attr] = file_path_to_img(context[attr])
                elif attr == 'given_Signal_SNR_Graph':
                    if norm_noisy_sig and norm_sig:
                        context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                        setattr(snr_DB, attr, context[attr])
                        context[attr] = file_path_to_img(context[attr])
                elif attr == 'given_Noise_SNR_Graph':
                    if norm_noisy_sig and norm_noise:
                        context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                        setattr(snr_DB, attr, context[attr])
                        context[attr] = file_path_to_img(context[attr])
                else:
                    if norm_sig and norm_noise or norm_noisy_sig and norm_sig or norm_noisy_sig and norm_noise or norm_noisy_sig and true_sig:
                        context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                        setattr(snr_DB, attr, context[attr])
                        context[attr] = file_path_to_img(context[attr])
            else:
                context[attr] = eval('file_path_to_img(snr_DB.' + attr + ')')
        snr_DB.save()
        context['type'] = 'SNR:detail'
        context['object'] = mic_Data_Record
        return context

class SNRRefreshedDetailView(generic.DetailView):
    model = SNRDatabase
    
    def get_context_data(self, **kwargs):
        context = super(SNRRefreshedDetailView, self).get_context_data(**kwargs)
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
        
        for attr, value in snr_DB_dict.items():
            if attr == 'pure_Signal_SNR_Graph':
                if norm_sig and norm_noise:
                    context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                    setattr(snr_DB, attr, context[attr])
                    context[attr] = file_path_to_img(context[attr])
            elif attr == 'system_Signal_SNR_Graph':
                if norm_noisy_sig and true_sig:
                    context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                    setattr(snr_DB, attr, context[attr])
                    context[attr] = file_path_to_img(context[attr])
            elif attr == 'given_Signal_SNR_Graph':
                if norm_noisy_sig and norm_sig:
                    context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                    setattr(snr_DB, attr, context[attr])
                    context[attr] = file_path_to_img(context[attr])
            elif attr == 'given_Noise_SNR_Graph':
                if norm_noisy_sig and norm_noise:
                    context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                    setattr(snr_DB, attr, context[attr])
                    context[attr] = file_path_to_img(context[attr])
            else:
                if norm_sig and norm_noise or norm_noisy_sig and norm_sig or norm_noisy_sig and norm_noise or norm_noisy_sig and true_sig:
                    context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                    setattr(snr_DB, attr, context[attr])
                    context[attr] = file_path_to_img(context[attr])
        snr_DB.save()
        context['type'] = 'SNR:detail-refreshed'
        context['object'] = mic_Data_Record
        return context

class PureSNRListView(generic.ListView):
    model = MicDataRecord
    template_name = 'snrDatabase/list_with_sidebar.html'
    
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
        context['type'] = 'SNR:pure-SNR-list-refreshed'
        return context

class PureSNRRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'snrDatabase/list_with_sidebar.html'
    
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
        context['type'] = 'SNR:pure-SNR-list-refreshed'
        return context

class SystemSNRListView(generic.ListView):
    model = MicDataRecord
    template_name = 'snrDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'SNR:system-SNR-list-refreshed'
        return context

class SystemSNRRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'snrDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'SNR:system-SNR-list-refreshed'
        return context

class SignalSNRListView(generic.ListView):
    model = MicDataRecord
    template_name = 'snrDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'SNR:signal-SNR-list-refreshed'
        return context

class SignalSNRRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'snrDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'SNR:signal-SNR-list-refreshed'
        return context

class NoiseSNRListView(generic.ListView):
    model = MicDataRecord
    template_name = 'snrDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'SNR:noise-SNR-list-refreshed'
        return context

class NoiseSNRRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'snrDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'SNR:noise-SNR-list-refreshed'
        return context

class AvgSNRDistanceListView(generic.ListView):
    model = MicDataRecord
    template_name = 'snrDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'SNR:avg-SNR-dist-list-refreshed'
        return context

class AvgSNRDistanceRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'snrDatabase/more_with_sidebar.html'
    
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
        context['type'] = 'SNR:avg-SNR-dist-list-refreshed'
        return context