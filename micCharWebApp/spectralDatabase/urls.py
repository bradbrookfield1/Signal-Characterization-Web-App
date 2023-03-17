from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

app_name = 'spectral'
urlpatterns = [
    path('', views.SpectralListView.as_view(), name='list'),
    path('<int:pk>/', views.SpectralDetailView.as_view(), name='detail'),
    path('<int:pk>/refreshed/', views.SpectralRefreshedDetailView.as_view(), name='detail-refreshed'),
    path('power-spectral-density-list/', views.PowerSpectralDensityListView.as_view(), name='power-spectral-density-list'),
    path('power-spectral-density-list/refreshed/', views.PowerSpectralDensityRefreshedListView.as_view(), name='power-spectral-density-list-refreshed'),
    path('phase-spectrum-list/', views.PhaseSpectrumListView.as_view(), name='phase-spectrum-list'),
    path('phase-spectrum-list/refreshed/', views.PhaseSpectrumRefreshedListView.as_view(), name='phase-spectrum-list-refreshed'),
    path('spectrogram-list/', views.SpectrogramListView.as_view(), name='spectrogram-list'),
    path('spectrogram-list/refreshed/', views.SpectrogramRefreshedListView.as_view(), name='spectrogram-list-refreshed'),
    path('mellin-spectrogram-list/', views.MellinListView.as_view(), name='mellin-spectrogram-list'),
    path('mellin-spectrogram-list/refreshed/', views.MellinRefreshedListView.as_view(), name='mellin-spectrogram-list-refreshed'),
    path('percussive-transform-list/', views.PercussiveComponentsListView.as_view(), name='percussive-components-list'),
    path('percussive-transform-list/refreshed/', views.PercussiveComponentsRefreshedListView.as_view(), name='percussive-components-list-refreshed'),
    path('harmonic-components-list/', views.HarmonicComponentsListView.as_view(), name='harmonic-components-list'),
    path('harmonic-components-list/refreshed/', views.HarmonicComponentsRefreshedListView.as_view(), name='harmonic-components-list-refreshed'),
    path('harmonic-prediction-list/', views.HarmonicPredictionListView.as_view(), name='harmonic-prediction-list'),
    path('harmonic-prediction-list/refreshed/', views.HarmonicPredictionRefreshedListView.as_view(), name='harmonic-prediction-list-refreshed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)