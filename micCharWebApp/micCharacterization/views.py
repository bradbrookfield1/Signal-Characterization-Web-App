from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.conf import settings
from django.utils import timezone
from .forms import MicDataRecordForm
from .models import MicDataRecord, Log
from .graphic_interfacing import charts_preprocess
from .graphs import (
    get_signal,
    get_PSD,
    get_spectrogram,
    get_PS,
    get_autocorrelation,
    get_percussive,
    get_harmonic,
    get_harmonic_transform,
)

class OriginalSignalListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/originalsignal_list.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_signal(norm_lib_list, norm_start_dur)
        return context

class PowerSpectralDensityListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/powerspectraldensity_list.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_PSD(norm_lib_list)
        return context

class SpectrogramListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/spectrogram_list.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_spectrogram(norm_lib_list)
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
    
class AutocorrelationListView(ListView):
    model = MicDataRecord
    template_name = 'micCharacterization/autocorrelation_list.html'
    
    def get_context_data(model):
        context = dict()
        file_set, start_dur_list = help_get_context()
        norm_lib_list, norm_start_dur = charts_preprocess(file_set, start_dur_list)
        context['graphs'] = get_autocorrelation(norm_lib_list)
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

class MicDataRecordListView(ListView):
    model = MicDataRecord

class MicDataRecordDetailView(DetailView):
    model = MicDataRecord
    
    def get_context_data(self, **kwargs):
        context = super(MicDataRecordDetailView, self).get_context_data(**kwargs)
        context['MEDIA_URL'] = settings.MEDIA_URL
        context['signal_File'] = self.get_object().sig_filename()
        context['reference_File'] = self.get_object().ref_filename()
        start_dur_list = self.get_object().get_start_dur()
        norm_lib_list, norm_start_dur = charts_preprocess(['./Uploads/' + context['signal_File']], [start_dur_list])
        context['time_signal'] = get_signal(norm_lib_list, norm_start_dur)[0]
        context['psd'] = get_PSD(norm_lib_list)[0]
        context['spectrogram'] = get_spectrogram(norm_lib_list)[0]
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

# class LogDeleteAllView(DeleteView):
#     model = Log
#     success_url = 'log-list'
    
#     def post(self, request):
#         objs = MicDataRecord.get_all_objects(MicDataRecord)
#         del objs
#         return super().post(request)
    
#     # def post(self, request):
#     #     MicDataRecord.objects.all().delete()
#     #     return super().post(request)
    
#     def get_success_url(self):
#         return reverse('log-list')