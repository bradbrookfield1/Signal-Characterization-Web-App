from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views, views_spectral_graphs, views_temporal_graphs

urlpatterns = [
    path('', views.MicDataRecordListView.as_view(), name='mic-data-record-list'),
    path('mic-data-record/<int:pk>/', views.MicDataRecordDetailView.as_view(), name='mic-data-record-detail'),
    path('new/', views.MicDataRecordCreateView.as_view(), name='mic-data-record-create'),
    path('mic-data-record/<int:pk>/update/', views.MicDataRecordUpdateView.as_view(), name='mic-data-record-update'),
    path('mic-data-record/<int:pk>/delete/', views.MicDataRecordDeleteView.as_view(), name='mic-data-record-confirm-delete'),
    path('logs/', views.LogListView.as_view(), name='log-list'),
    path('logs/<int:pk>/delete/', views.LogDeleteView.as_view(), name='log-confirm-delete'),
    path('logs/delete/all/', views.delete_all_logs, name='log-confirm-delete-all'),
    path('important-concepts', views.ImportantConceptsView.as_view(), name='concepts'),
    path('test', views.TestView.as_view(), name='test-view'),
    
    path('original-signal-list/', views_temporal_graphs.OriginalSignalListView.as_view(), name='original-signal-list'),
    path('cepstrum-list/', views_temporal_graphs.CepstrumListView.as_view(), name='cepstrum-list'),
    path('hilbert-phase-list/', views_temporal_graphs.HilbertPhaseListView.as_view(), name='hilbert-phase-list'),
    path('onset-strength-list/', views_temporal_graphs.OnsetStrengthListView.as_view(), name='onset-strength-list'),
    path('autocorrelation-lag-list/', views_temporal_graphs.AutocorrelationLagListView.as_view(), name='autocorrelation-lag-list'),
    path('autocorrelation-bpm-list/', views_temporal_graphs.AutocorrelationBPMListView.as_view(), name='autocorrelation-bpm-list'),
    path('autocorrelation-tempogram-list/', views_temporal_graphs.AutocorrTempogramListView.as_view(), name='autocorrelation-tempogram-list'),
    path('fourier-tempogram-list/', views_temporal_graphs.FourierTempogramListView.as_view(), name='fourier-tempogram-list'),
    
    path('power-spectral-density-list/', views_spectral_graphs.PowerSpectralDensityListView.as_view(), name='power-spectral-density-list'),
    path('phase-spectrum-list/', views_spectral_graphs.PhaseSpectrumListView.as_view(), name='phase-spectrum-list'),
    path('harmonic-prediction-list/', views_spectral_graphs.HarmonicPredictionListView.as_view(), name='harmonic-prediction-list'),
    path('power-spectrum-list/', views_spectral_graphs.PowerSpectrumListView.as_view(), name='power-spectrum-list'),
    path('mellin-spectrum-list/', views_spectral_graphs.MellinListView.as_view(), name='mellin-spectrum-list'),
    path('percussive-transform-list/', views_spectral_graphs.PercussiveComponentsListView.as_view(), name='percussive-components-list'),
    path('harmonic-components-list/', views_spectral_graphs.HarmonicComponentsListView.as_view(), name='harmonic-components-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)