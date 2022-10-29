from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import (
    OriginalSignalListView,
    PowerSpectralDensityListView,
    SpectrogramListView,
    PercussiveTransformListView,
    HarmonicTransformListView,
    MicDataRecordListView,
    MicDataRecordDetailView,
    MicDataRecordCreateView,
    MicDataRecordUpdateView,
    MicDataRecordDeleteView,
    LogListView,
    LogDeleteView,
    # LogDeleteAllView,
)

urlpatterns = [
    path('', MicDataRecordListView.as_view(), name='mic-data-record-list'),
    path('mic-data-record/<int:pk>/', MicDataRecordDetailView.as_view(), name='mic-data-record-detail'),
    path('new/', MicDataRecordCreateView.as_view(), name='mic-data-record-create'),
    path('mic-data-record/<int:pk>/update/', MicDataRecordUpdateView.as_view(), name='mic-data-record-update'),
    path('mic-data-record/<int:pk>/delete/',
         MicDataRecordDeleteView.as_view(), name='mic-data-record-confirm-delete'),
    path('logs/', LogListView.as_view(), name='log-list'),
    path('logs/<int:pk>/delete/',
         LogDeleteView.as_view(), name='log-confirm-delete'),
    # path('logs/delete/all/', LogDeleteAllView.as_view(), name='log-confirm-delete-all'),
    path('original-signal-list/', OriginalSignalListView.as_view(), name='original-signal-list'),
    path('power-spectral-density-list/', PowerSpectralDensityListView.as_view(), name='power-spectral-density-list'),
    path('spectrogram-list/', SpectrogramListView.as_view(), name='spectrogram-list'),
    path('percussive-transform-list/', PercussiveTransformListView.as_view(), name='percussive-transform-list'),
    path('harmonic-transform-list/', HarmonicTransformListView.as_view(), name='harmonic-transform-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)