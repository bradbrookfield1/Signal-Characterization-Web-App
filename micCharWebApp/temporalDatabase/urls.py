from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

app_name = 'temporal'
urlpatterns = [
    path('', views.TemporalListView.as_view(), name='list'),
    path('<int:pk>/', views.TemporalDetailView.as_view(), name='detail'),
    path('<int:pk>/refreshed/', views.TemporalRefreshedDetailView.as_view(), name='detail-refreshed'),
    path('original-signal-list/', views.OriginalSignalListView.as_view(), name='original-signal-list'),
    path('original-signal-list/refreshed/', views.OriginalSignalRefreshedListView.as_view(), name='original-signal-list-refreshed'),
    path('cepstrum-list/', views.CepstrumListView.as_view(), name='cepstrum-list'),
    path('cepstrum-list/refreshed/', views.CepstrumRefreshedListView.as_view(), name='cepstrum-list-refreshed'),
    path('hilbert-phase-list/', views.HilbertPhaseListView.as_view(), name='hilbert-phase-list'),
    path('hilbert-phase-list/refreshed/', views.HilbertPhaseRefreshedListView.as_view(), name='hilbert-phase-list-refreshed'),
    path('onset-strength-list/', views.OnsetStrengthListView.as_view(), name='onset-strength-list'),
    path('onset-strength-list/refreshed/', views.OnsetStrengthRefreshedListView.as_view(), name='onset-strength-list-refreshed'),
    path('autocorrelation-lag-list/', views.AutocorrelationLagListView.as_view(), name='autocorrelation-lag-list'),
    path('autocorrelation-lag-list/refreshed/', views.AutocorrelationLagRefreshedListView.as_view(), name='autocorrelation-lag-list-refreshed'),
    path('autocorrelation-bpm-list/', views.AutocorrelationBPMListView.as_view(), name='autocorrelation-bpm-list'),
    path('autocorrelation-bpm-list/refreshed/', views.AutocorrelationBPMRefreshedListView.as_view(), name='autocorrelation-bpm-list-refreshed'),
    path('autocorrelation-tempogram-list/', views.AutocorrTempogramListView.as_view(), name='autocorrelation-tempogram-list'),
    path('autocorrelation-tempogram-list/refreshed/', views.AutocorrTempogramRefreshedListView.as_view(), name='autocorrelation-tempogram-list-refreshed'),
    path('fourier-tempogram-list/', views.FourierTempogramListView.as_view(), name='fourier-tempogram-list'),
    path('fourier-tempogram-list/refreshed/', views.FourierTempogramRefreshedListView.as_view(), name='fourier-tempogram-list-refreshed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)