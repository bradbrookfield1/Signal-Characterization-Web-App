from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

app_name = 'SNR'
urlpatterns = [
    path('', views.SNRListView.as_view(), name='list'),
    path('<int:pk>/', views.SNRDetailView.as_view(), name='detail'),
    path('<int:pk>/refreshed/', views.SNRRefreshedDetailView.as_view(), name='detail-refreshed'),
    path('pure-SNR-list/', views.PureSNRListView.as_view(), name='pure-SNR-list'),
    path('pure-SNR-list/refreshed/', views.PureSNRRefreshedListView.as_view(), name='pure-SNR-list-refreshed'),
    path('system-SNR-list/', views.SystemSNRListView.as_view(), name='system-SNR-list'),
    path('system-SNR-list/refreshed/', views.SystemSNRRefreshedListView.as_view(), name='system-SNR-list-refreshed'),
    path('signal-SNR-list/', views.SignalSNRListView.as_view(), name='signal-SNR-list'),
    path('signal-SNR-list/refreshed/', views.SignalSNRRefreshedListView.as_view(), name='signal-SNR-list-refreshed'),
    path('noise-SNR-list/', views.NoiseSNRListView.as_view(), name='noise-SNR-list'),
    path('noise-SNR-list/refreshed/', views.NoiseSNRRefreshedListView.as_view(), name='noise-SNR-list-refreshed'),
    path('avg-SNR-dist-list/', views.AvgSNRDistanceListView.as_view(), name='avg-SNR-dist-list'),
    path('avg-SNR-dist-list/refreshed/', views.AvgSNRDistanceRefreshedListView.as_view(), name='avg-SNR-dist-list-refreshed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)