from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models.deletion import Collector
from django.db import router
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.conf import settings
from django.utils import timezone
from .forms import MicDataRecordForm, DeleteAllForm
from .models import MicDataRecord, Log
from .graphic_interfacing import charts_preprocess
from .graphs import (
    get_signal,
    get_avg_power,
    get_PS,
    get_lag_autocorrelation,
    get_bpm_autocorrelation,
    get_onset_strength,
    get_fourier_tempogram,
    get_autocorr_tempogram,
    get_percussive,
    get_harmonic,
    get_harmonic_transform,
    get_mellin
)

class OriginalSignalListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/list_without_sidebar.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_signal(norm_lib_list, norm_start_dur)
        return context

class OnsetStrengthListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/onsetstrength_list.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_onset_strength(norm_lib_list)
        return context
    
class AutocorrelationLagListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/list_with_sidebar.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_lag_autocorrelation(norm_lib_list)
        return context
    
class AutocorrelationBPMListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/autocorrelationbpm_list.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_bpm_autocorrelation(norm_lib_list)
        return context
    
class AutocorrTempogramListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/autocorrtempogram_list.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_autocorr_tempogram(norm_lib_list)
        return context
    
class FourierTempogramListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/fouriertempogram_list.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_fourier_tempogram(norm_lib_list)
        return context

class AveragePowerListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/averagepower_list.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_avg_power(norm_lib_list)
        return context

class PowerSpectrumListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/powerspectrum_list.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_PS(norm_lib_list)
        return context

class MellinListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/mellin_list.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_mellin(norm_lib_list)
        return context

class PercussiveComponentsListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/percussivecomponents_list.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_percussive(norm_lib_list)
        return context

class HarmonicComponentsListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/harmoniccomponents_list.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_harmonic(norm_lib_list)
        return context

class HarmonicTransformListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/harmonictransform_list.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_harmonic_transform(norm_lib_list)
        return context

class ImportantConceptsView(TemplateView):
    template_name = 'micCharacterization/important_concepts.html'

class MicDataRecordListView(ListView):
    model = MicDataRecord

class MicDataRecordDetailView(DetailView):
    model = MicDataRecord
    
    def get_context_data(self, **kwargs):
        context = super(MicDataRecordDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        context['MEDIA_URL'] = settings.MEDIA_URL
        context['signal_File'] = obj.sig_filename()
        context['reference_File'] = obj.ref_filename()
        start_dur_list = obj.get_start_dur()
        norm_lib_list, norm_start_dur = charts_preprocess(['./Uploads/' + context['signal_File']], [start_dur_list])
        context['time_signal'] = get_signal(norm_lib_list, norm_start_dur)[0]
        context['ps'] = get_PS(norm_lib_list)[0]
        context['lag_autocorrelation'] = get_lag_autocorrelation(norm_lib_list)[0]
        context['bpm_autocorrelation'] = get_bpm_autocorrelation(norm_lib_list)[0]
        context['onset_strength'] = get_onset_strength(norm_lib_list)[0]
        context['fourier_tempogram'] = get_fourier_tempogram(norm_lib_list)[0]
        context['autocorrelation_tempogram'] = get_autocorr_tempogram(norm_lib_list)[0]
        context['average_power'] = get_avg_power(norm_lib_list)[0]
        context['percussive'] = get_percussive(norm_lib_list)[0]
        context['harmonic'] = get_harmonic(norm_lib_list)[0]
        context['mellin'] = get_mellin(norm_lib_list)[0]
        return context

class MicDataRecordCreateView(CreateView):
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

class MicDataRecordUpdateView(UpdateView):
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

class MicDataRecordDeleteView(DeleteView):
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

class LogListView(ListView):
    model = Log

class LogDeleteView(DeleteView):
    model = Log
    success_url = 'log-list'

    def get_success_url(self):
        return reverse('log-list')

def help_get_context():
    file_set_list = MicDataRecord.get_fileset()
    records = MicDataRecord.objects.all()
    file_set = []
    start_dur_list = []
    for idx, f in enumerate(file_set_list):
        file_set.append('./Uploads/' + f)
        start_dur_list.append(records[idx].get_start_dur())
    return file_set, start_dur_list

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