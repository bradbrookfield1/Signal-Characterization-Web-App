from django.views import generic
from micCharacterization.models import MicDataRecord
from micCharacterization.views_functions import find_graph, list_intro, help_get_context, detail_intro
from micCharacterization.graphic_interfacing import file_path_to_img
from .models import StatisticalDatabase

class StatisticalListView(generic.ListView):
    model = MicDataRecord
    template_name = 'statisticalDatabase/statisticaldatabase_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(StatisticalListView, self).get_context_data(**kwargs)
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

class StatisticalDetailView(generic.DetailView):
    model = StatisticalDatabase
    
    def get_context_data(self, **kwargs):
        context = super(StatisticalDetailView, self).get_context_data(**kwargs)
        mic_Data_Record = self.get_object().mic_Data_Record
        name = str(mic_Data_Record)
        context, norm_noisy_sig, norm_sig, norm_noise, true_sig, temp_DB_dict, spec_DB_dict, snr_DB_dict, stat_DB_dict, temp_DB, spec_DB, snr_DB, stat_DB = detail_intro(context, mic_Data_Record)
        
        for attr, value in stat_DB_dict.items():
            if value == None:
                context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                setattr(stat_DB, attr, context[attr])
                context[attr] = file_path_to_img(context[attr])
            else:
                context[attr] = eval('file_path_to_img(stat_DB.' + attr + ')')
        stat_DB.save()
        context['type'] = 'stat:detail'
        context['object'] = mic_Data_Record
        return context

class StatisticalRefreshedDetailView(generic.DetailView):
    model = StatisticalDatabase
    
    def get_context_data(self, **kwargs):
        context = super(StatisticalRefreshedDetailView, self).get_context_data(**kwargs)
        mic_Data_Record = self.get_object().mic_Data_Record
        name = str(mic_Data_Record)
        context, norm_noisy_sig, norm_sig, norm_noise, true_sig, temp_DB_dict, spec_DB_dict, snr_DB_dict, stat_DB_dict, temp_DB, spec_DB, snr_DB, stat_DB = detail_intro(context, mic_Data_Record)
        
        for attr, value in stat_DB_dict.items():
            context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
            setattr(stat_DB, attr, context[attr])
            context[attr] = file_path_to_img(context[attr])
        stat_DB.save()
        context['type'] = 'stat:detail-refreshed'
        context['object'] = mic_Data_Record
        return context