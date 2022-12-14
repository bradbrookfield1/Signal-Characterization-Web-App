from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models.deletion import Collector
from django.db import router
from django.views import generic
from django.conf import settings
from django.utils import timezone
from .forms import MicDataRecordForm, DeleteAllForm
from .models import MicDataRecord, Log
from .graphic_interfacing import charts_preprocess
from . import graphs_temporal, graphs_spectral

class ImportantConceptsView(generic.TemplateView):
    template_name = 'micCharacterization/important_concepts.html'

class TestView(generic.TemplateView):
    template_name = 'micCharacterization/test.html'
    
    def get_context_data(self, **kwargs):
        context = dict()
        context['file_set'], context['start_dur_list'], context['name_list'] = help_get_context()        
        return context

class MicDataRecordListView(generic.ListView):
    model = MicDataRecord

class MicDataRecordDetailView(generic.DetailView):
    model = MicDataRecord
    
    def get_context_data(self, **kwargs):
        context = super(MicDataRecordDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        name = str(obj)
        context['MEDIA_URL'] = settings.MEDIA_URL
        context['signal_File'] = obj.sig_filename()
        context['reference_File'] = obj.ref_filename()
        start_dur_list = obj.get_start_dur()
        
        norm_lib_list, norm_start_dur, norm_sig_list = charts_preprocess(['./Uploads/' + context['signal_File']], [start_dur_list])
        context['time_signal'] = graphs_temporal.get_signal(norm_lib_list, norm_start_dur, norm_sig_list, name)[0]
        context['cepstrum'] = graphs_temporal.get_cepstrum(norm_lib_list, norm_sig_list, name)[0]
        context['inst_phase'] = graphs_temporal.get_inst_phase(norm_lib_list, norm_sig_list, name)[0]
        context['onset_strength'] = graphs_temporal.get_onset_strength(norm_lib_list, name)[0]
        context['lag_autocorrelation'] = graphs_temporal.get_lag_autocorrelation(norm_lib_list, name)[0]
        context['bpm_autocorrelation'] = graphs_temporal.get_bpm_autocorrelation(norm_lib_list, name)[0]
        context['autocorrelation_tempogram'] = graphs_temporal.get_autocorr_tempogram(norm_lib_list, name)[0]
        context['fourier_tempogram'] = graphs_temporal.get_fourier_tempogram(norm_lib_list, name)[0]
        
        context['psd'] = graphs_spectral.get_PSD(norm_lib_list, name)[0]
        context['phase_spectrum'] = graphs_spectral.get_phase_spectrum(norm_sig_list, name)[0]
        # context['harmonic_prediction'] = graphs_spectral.get_harmonic_prediction(norm_lib_list, [obj.prediction_Harmonics], name)[0]
        context['ps'] = graphs_spectral.get_PS(norm_lib_list, name)[0]
        context['mellin'] = graphs_spectral.get_mellin(norm_lib_list, name)[0]
        context['percussive'] = graphs_spectral.get_percussive(norm_lib_list, name)[0]
        context['harmonic'] = graphs_spectral.get_harmonic(norm_lib_list, name)[0]
        return context

class MicDataRecordCreateView(generic.CreateView):
    model = MicDataRecord
    form_class = MicDataRecordForm
    
    def get_context_data(self, **kwargs):
        context = super(MicDataRecordCreateView, self).get_context_data(**kwargs)
        context['isUpdate'] = False
        return context

    def form_valid(self, form):
        record_Name = form.cleaned_data['record_Name']
        log = Log(action='Created', log_Name=record_Name, date=timezone.now())
        log.save()
        messages.success(self.request, f'Data record made for {record_Name}!')
        return super().form_valid(form)

class MicDataRecordUpdateView(generic.UpdateView):
    model = MicDataRecord
    form_class = MicDataRecordForm

    def get_context_data(self, **kwargs):
        context = super(MicDataRecordUpdateView, self).get_context_data(**kwargs)
        context['isUpdate'] = True
        return context

    def form_valid(self, form):
        record_Name = form.cleaned_data['record_Name']
        log = Log(action="Updated", log_Name=record_Name, date=timezone.now())
        log.save()
        messages.success(self.request, f'Data record updated for {record_Name}!')
        return super().form_valid(form)

class MicDataRecordDeleteView(generic.DeleteView):
    model = MicDataRecord
    success_url = 'mic-data-record-list'

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        log = Log(action="Deleted", log_Name=obj.record_Name, date=timezone.now())
        log.save()
        messages.success(self.request, f'Data record deleted for {obj.record_Name}!')
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

def help_get_context():
    file_set_list = MicDataRecord.get_fileset()
    records = MicDataRecord.objects.all()
    file_set = []
    start_dur_list = []
    name_list = []
    i = range(len(records))
    for idx, f, rec in zip(i, file_set_list, records):
        file_set.append('./Uploads/' + f)
        start_dur_list.append(records[idx].get_start_dur())
        name_list.append(rec.record_Name)
    return file_set, start_dur_list, name_list

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