from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models.deletion import Collector
from django.db import router
from django.views import generic
from django.utils import timezone
# from django.forms import ValidationError
from .forms import MicDataRecordForm, DeleteAllForm
from .models import MicDataRecord, Log, TemporalDatabase, SpectralDatabase
from .views_custom_functions import detail_intro, find_graph, delete_intro, help_get_context, spec_prop_abs_coeff_graphs
from .graphic_interfacing import file_path_to_img
import copy, os

class MicDataRecordListView(generic.ListView):
    model = MicDataRecord
    
    def get_context_data(self, **kwargs):
        context = super(MicDataRecordListView, self).get_context_data(**kwargs)
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

class MicDataRecordDetailView(generic.DetailView):
    model = MicDataRecord
    
    def get_context_data(self, **kwargs):
        context = super(MicDataRecordDetailView, self).get_context_data(**kwargs)
        mic_Data_Record = self.get_object()
        name = str(mic_Data_Record)
        context, norm_noisy_sig, norm_sig, norm_noise, true_sig, temp_DB_dict, spec_DB_dict, temp_DB, spec_DB = detail_intro(context, mic_Data_Record)
        temp_DB_fixed = copy.deepcopy(temp_DB_dict)
        spec_DB_fixed = copy.deepcopy(spec_DB_dict)
        # del temp_DB_fixed['_state'], temp_DB_fixed['id'], temp_DB_fixed['mic_Data_Record_id']
        # del spec_DB_fixed['_state'], spec_DB_fixed['id'], spec_DB_fixed['mic_Data_Record_id']
        
        for attr, value in temp_DB_fixed.items():
            if value == None:
                context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                setattr(temp_DB, attr, context[attr])
                context[attr] = file_path_to_img(context[attr])
            else:
                context[attr] = eval('file_path_to_img(temp_DB.' + attr + ')')
        for attr, value in spec_DB_fixed.items():
            if value == None:
                if attr == 'pure_Signal_SNR_Graph':
                    if norm_sig and norm_noise:
                        context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                        setattr(spec_DB, attr, context[attr])
                        context[attr] = file_path_to_img(context[attr])
                elif attr == 'given_Signal_SNR_Graph':
                    if norm_noisy_sig and norm_sig:
                        context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                        setattr(spec_DB, attr, context[attr])
                        context[attr] = file_path_to_img(context[attr])
                elif attr == 'given_Noise_SNR_Graph':
                    if norm_noisy_sig and norm_noise:
                        context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                        setattr(spec_DB, attr, context[attr])
                        context[attr] = file_path_to_img(context[attr])
                elif attr == 'system_Signal_SNR_Graph':
                    if norm_noisy_sig and true_sig:
                        context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                        setattr(spec_DB, attr, context[attr])
                        context[attr] = file_path_to_img(context[attr])
                else:
                    context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                    setattr(spec_DB, attr, context[attr])
                    context[attr] = file_path_to_img(context[attr])
            else:
                context[attr] = eval('file_path_to_img(spec_DB.' + attr + ')')
        temp_DB.save()
        spec_DB.save()
        context['type'] = 'mic-data-record-detail'
        return context

class MicDataRecordRefreshedDetailView(generic.DetailView):
    model = MicDataRecord
    
    def get_context_data(self, **kwargs):
        context = super(MicDataRecordRefreshedDetailView, self).get_context_data(**kwargs)
        mic_Data_Record = self.get_object()
        name = str(mic_Data_Record)
        context, norm_noisy_sig, norm_sig, norm_noise, true_sig, temp_DB_dict_fixed, spec_DB_dict_fixed, temp_DB, spec_DB = detail_intro(context, mic_Data_Record)
        
        for attr, value in temp_DB_dict_fixed.items():
            context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
            setattr(temp_DB, attr, context[attr])
            context[attr] = file_path_to_img(context[attr])
        for attr, value in spec_DB_dict_fixed.items():
            if attr == 'pure_Signal_SNR_Graph':
                if norm_sig and norm_noise:
                    context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                    setattr(spec_DB, attr, context[attr])
                    context[attr] = file_path_to_img(context[attr])
            elif attr == 'system_Signal_SNR_Graph':
                if norm_noisy_sig and true_sig:
                    context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                    setattr(spec_DB, attr, context[attr])
                    context[attr] = file_path_to_img(context[attr])
            elif attr == 'given_Signal_SNR_Graph':
                if norm_noisy_sig and norm_sig:
                    context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                    setattr(spec_DB, attr, context[attr])
                    context[attr] = file_path_to_img(context[attr])
            elif attr == 'given_Noise_SNR_Graph':
                if norm_noisy_sig and norm_noise:
                    context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                    setattr(spec_DB, attr, context[attr])
                    context[attr] = file_path_to_img(context[attr])
            else:
                context = find_graph(attr, context, name, norm_noisy_sig, norm_sig, norm_noise, true_sig, mic_Data_Record)
                setattr(spec_DB, attr, context[attr])
                context[attr] = file_path_to_img(context[attr])
        temp_DB.save()
        spec_DB.save()
        context['type'] = 'mic-data-record-detail-refreshed'
        return context

class MicDataRecordCreateView(generic.CreateView):
    model = MicDataRecord
    form_class = MicDataRecordForm
    success_url = 'mic-data-record-list'
    
    def get_context_data(self, **kwargs):
        context = super(MicDataRecordCreateView, self).get_context_data(**kwargs)
        context['type'] = 'mic-data-record-create'
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        temporal_Database = TemporalDatabase(mic_Data_Record=self.object, signal_Graph=None, cepstrum_Graph=None, hilbert_Phase_Graph=None, onset_Strength_Graph=None, lag_Autocorrelation_Graph=None, BPM_Autocorrelation_Graph=None, autocorrelation_Tempogram=None, fourier_Tempogram=None)
        temporal_Database.save()
        spectral_Database = SpectralDatabase(mic_Data_Record=self.object, average_PSD_Graph=None, phase_Spectrum_Graph=None, pure_Signal_SNR_Graph=None, system_Signal_SNR_Graph=None, given_Signal_SNR_Graph=None, given_Noise_SNR_Graph=None, spectrogram=None, mellin_Spectrogram=None, percussive_Spectrogram=None, harmonic_Spectrogram=None, harmonic_Prediction_Graph=None)
        spectral_Database.save()
        record_Name = form.cleaned_data['record_Name']
        log = Log(action='Created', record_Name=record_Name, date=timezone.now())
        log.save()
        messages.success(self.request, f'Data record made for {record_Name}!')
        return HttpResponseRedirect(reverse(self.get_success_url()))

class MicDataRecordUpdateView(generic.UpdateView):
    model = MicDataRecord
    form_class = MicDataRecordForm

    def get_context_data(self, **kwargs):
        context = super(MicDataRecordUpdateView, self).get_context_data(**kwargs)
        context['type'] = 'mic-data-record-update'
        return context

    def form_valid(self, form):
        record_Name = form.cleaned_data['record_Name']
        log = Log(action="Updated", record_Name=record_Name, date=timezone.now())
        log.save()
        messages.success(self.request, f'Data record updated for {record_Name}!')
        return super().form_valid(form)

class MicDataRecordDeleteView(generic.DeleteView):
    model = MicDataRecord
    success_url = 'mic-data-record-list'

    def post(self, request, *args, **kwargs):
        mic_Data_Record = self.get_object()
        temp_DB_dict_fixed, spec_DB_dict_fixed = delete_intro(mic_Data_Record)
        for attr, value in temp_DB_dict_fixed.items():
            full_name = 'Uploads/Temporal Graphs/' + attr + '/' + attr + '_' + str(mic_Data_Record.pk) + '.png'
            if os.path.exists(full_name):
                os.remove(full_name)
        for attr, value in spec_DB_dict_fixed.items():
            full_name = 'Uploads/Spectral Graphs/' + attr + '/' + attr + '_' + str(mic_Data_Record.pk) + '.png'
            if os.path.exists(full_name):
                os.remove(full_name)
        
        log = Log(action="Deleted", record_Name=mic_Data_Record.record_Name, date=timezone.now())
        log.save()
        messages.success(self.request, f'Data record deleted for {mic_Data_Record.record_Name}!')
        return super().post(request)

    def get_success_url(self):
        return reverse('mic-data-record-list')

class LogListView(generic.ListView):
    model = Log

class LogDeleteView(generic.DeleteView):
    model = Log
    success_url = 'log-list'

    def get_success_url(self):
        return reverse('log-list')

def delete_all_logs(request):
    if request.method == 'POST':
        form = DeleteAllForm(request.POST)
        if form.is_valid():
            logs = Log.get_all_logs()
            for log in logs:
                using = router.db_for_write(log.__class__, instance=log)
                collector = Collector(using=using, origin=log)
                collector.collect([log], keep_parents=False)
                collector.delete()
            return redirect('log-list')
    else:
        form = DeleteAllForm()
    return render(request, 'micCharacterization/log_confirm_delete_all.html')

class ImportantConceptsView(generic.TemplateView):
    template_name = 'micCharacterization/important_concepts.html'

class AcousticPropagationView(generic.TemplateView):
    template_name = 'micCharacterization/acoustic_propagation.html'
    
    def get_context_data(self):
        context = dict()
        context['graphs'] = spec_prop_abs_coeff_graphs()
        return context

class TestView(generic.TemplateView):
    template_name = 'micCharacterization/test.html'
    
    def get_context_data(self, **kwargs):
        context = dict()
        temp_DB = TemporalDatabase.objects.first()
        context['temp_DB_Graphs'] = temp_DB.attributes()
        # context['file_set'], context['start_dur_list'], context['name_list'] = help_get_context()    
        context['type'] = 'test-view'
        return context