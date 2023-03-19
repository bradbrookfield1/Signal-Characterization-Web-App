from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models.deletion import Collector
from django.db import router
from django.views import generic
from django.utils import timezone
from .forms import MicDataRecordForm, DeleteAllForm
from .models import MicDataRecord, Log
from temporalDatabase.models import TemporalDatabase
from spectralDatabase.models import SpectralDatabase
from snrDatabase.models import SNRDatabase
from statisticalDatabase.models import StatisticalDatabase
from .views_functions import delete_intro, help_get_context, spec_prop_abs_coeff_graphs, save_hpss_files
import os

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

class MicDataRecordCreateView(generic.CreateView):
    model = MicDataRecord
    form_class = MicDataRecordForm
    success_url = 'mic-characterization:mic-data-record-list'
    
    def get_context_data(self, **kwargs):
        context = super(MicDataRecordCreateView, self).get_context_data(**kwargs)
        context['type'] = 'mic-characterization:mic-data-record-create'
        return context
    
    def form_valid(self, form):
        file_fields = ['noisy_Signal_File', 'measured_Signal_File', 'noise_File', 'true_Signal_File']
        file_paths = []
        file_names = []
        for field in file_fields:
            if form.cleaned_data[field]:
                file_paths.append(self.request.FILES.get(field).file.name)
                file_names.append(form.cleaned_data[field].name)
            else:
                file_paths.append(None)
                file_names.append(None)
        self.object = form.save()
        save_hpss_files(self.object, file_paths, file_names)
        temporal_Database = TemporalDatabase(mic_Data_Record=self.object, signal_Graph=None, cepstrum_Graph=None, hilbert_Phase_Graph=None, onset_Strength_Graph=None, lag_Autocorrelation_Graph=None, BPM_Autocorrelation_Graph=None, autocorrelation_Tempogram=None, fourier_Tempogram=None)
        temporal_Database.save()
        spectral_Database = SpectralDatabase(mic_Data_Record=self.object, average_PSD_Graph=None, phase_Spectrum_Graph=None, spectrogram=None, mellin_Spectrogram=None, percussive_Spectrogram=None, harmonic_Spectrogram=None, harmonic_Prediction_Graph=None)
        spectral_Database.save()
        snr_Database = SNRDatabase(mic_Data_Record=self.object, pure_Signal_SNR_Graph=None, system_Signal_SNR_Graph=None, given_Signal_SNR_Graph=None, given_Noise_SNR_Graph=None, average_SNR_Distance_Graph=None)
        snr_Database.save()
        stat_Database = StatisticalDatabase(mic_Data_Record=self.object)
        stat_Database.save()
        record_Name = form.cleaned_data['record_Name']
        log = Log(action='Created', record_Name=record_Name, date=timezone.now())
        log.save()
        messages.success(self.request, f'Data record made for {record_Name}!')
        return HttpResponseRedirect(reverse(self.get_success_url()))

class MicDataRecordUpdateView(generic.UpdateView):
    model = MicDataRecord
    form_class = MicDataRecordForm
    success_url = 'mic-characterization:mic-data-record-list'

    def get_context_data(self, **kwargs):
        context = super(MicDataRecordUpdateView, self).get_context_data(**kwargs)
        context['type'] = 'mic-characterization:mic-data-record-update'
        return context

    def form_valid(self, form):
        file_fields = ['noisy_Signal_File', 'measured_Signal_File', 'noise_File', 'true_Signal_File']
        file_paths = []
        file_names = []
        for field in file_fields:
            if not self.request.FILES.get(field) == None:
                file_paths.append(self.request.FILES.get(field).file.name)
                file_names.append(form.cleaned_data[field].name)
            else:
                file_paths.append(None)
                file_names.append(None)
        save_hpss_files(self.object, file_paths, file_names)
        record_Name = form.cleaned_data['record_Name']
        log = Log(action="Updated", record_Name=record_Name, date=timezone.now())
        log.save()
        messages.success(self.request, f'Data record updated for {record_Name}!')
        self.object = form.save()
        return HttpResponseRedirect(reverse(self.get_success_url()))

class MicDataRecordDeleteView(generic.DeleteView):
    model = MicDataRecord
    success_url = 'mic-characterization:mic-data-record-list'

    def post(self, request, *args, **kwargs):
        mic_Data_Record = self.get_object()
        temp_DB_dict_fixed, spec_DB_dict_fixed, snr_DB_dict_fixed, stat_DB_dict_fixed = delete_intro(mic_Data_Record)
        for attr, value in temp_DB_dict_fixed.items():
            full_name = 'Uploads/Temporal Graphs/' + attr + '/' + attr + '_' + str(mic_Data_Record.pk) + '.png'
            if os.path.exists(full_name):
                os.remove(full_name)
        for attr, value in spec_DB_dict_fixed.items():
            full_name = 'Uploads/Spectral Graphs/' + attr + '/' + attr + '_' + str(mic_Data_Record.pk) + '.png'
            if os.path.exists(full_name):
                os.remove(full_name)
        for attr, value in snr_DB_dict_fixed.items():
            full_name = 'Uploads/SNR Graphs/' + attr + '/' + attr + '_' + str(mic_Data_Record.pk) + '.png'
            if os.path.exists(full_name):
                os.remove(full_name)
        for attr, value in stat_DB_dict_fixed.items():
            full_name = 'Uploads/Statistical Graphs/' + attr + '/' + attr + '_' + str(mic_Data_Record.pk) + '.png'
            if os.path.exists(full_name):
                os.remove(full_name)
        
        log = Log(action="Deleted", record_Name=mic_Data_Record.record_Name, date=timezone.now())
        log.save()
        messages.success(self.request, f'Data record deleted for {mic_Data_Record.record_Name}!')
        return super().post(request)

    def get_success_url(self):
        return reverse('mic-characterization:mic-data-record-list')

class LogListView(generic.ListView):
    model = Log

class LogDeleteView(generic.DeleteView):
    model = Log
    success_url = 'mic-characterization:log-list'

    def get_success_url(self):
        return reverse('mic-characterization:log-list')

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
            return redirect('mic-characterization:log-list')
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
        context['type'] = 'mic-characterization:test-view'
        return context