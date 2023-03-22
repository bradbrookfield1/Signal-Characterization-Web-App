from django.views import generic
from micCharacterization.models import MicDataRecord
from micCharacterization.views_functions import find_graph, list_intro, help_get_context, detail_intro
from micCharacterization.graphic_interfacing import file_path_to_img
from .models import StatisticalDatabase
from .graphs import assign_hpss_arrays

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
        context, hpss_array = assign_hpss_arrays(context, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
        
        for attr, value in stat_DB_dict.items():
            if value == None:
                context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record, hpss_array)
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
        context, hpss_array = assign_hpss_arrays(context, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
        
        for attr, value in stat_DB_dict.items():
            context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record, hpss_array)
            setattr(stat_DB, attr, context[attr])
            context[attr] = file_path_to_img(context[attr])
        stat_DB.save()
        context['type'] = 'stat:detail-refreshed'
        context['object'] = mic_Data_Record
        return context
    
class OriginalPDFListView(generic.ListView):
    model = MicDataRecord
    template_name = 'statisticalDatabase/list_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Statistical')
        path_list = db_list.values_list('original_PDF_Graph', flat=True)
        good_graph_list = []
        
        for path, norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(path_list, norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            if path == None:
                context = find_graph('original_PDF_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
                db.original_PDF_Graph = context['original_PDF_Graph']
                db.save()
                good_graph_list.append(file_path_to_img(context['original_PDF_Graph']))
            else:
                good_graph_list.append(file_path_to_img(path))
        context['graphs'] = good_graph_list
        context['type'] = 'stat:original-PDFs-list-refreshed'
        return context

class OriginalPDFRefreshedListView(generic.ListView):
    model = MicDataRecord
    template_name = 'statisticalDatabase/list_with_sidebar.html'
    
    def get_context_data(self):
        context = dict()
        norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, records, db_list = list_intro('Statistical')
        path_list = db_list.values_list('original_PDF_Graph', flat=True)
        good_graph_list = []
        
        for norm_noisy_sig, norm_sig, norm_noise, true_sig, name, db, rec in zip(norm_noisy_sig_list, norm_sig_list, norm_noise_list, true_sig_list, name_list, db_list, records):
            context = find_graph('original_PDF_Graph', context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, rec)
            db.original_PDF_Graph = context['original_PDF_Graph']
            db.save()
            good_graph_list.append(file_path_to_img(context['original_PDF_Graph']))
        context['graphs'] = good_graph_list
        context['type'] = 'stat:original-PDFs-list-refreshed'
        return context