from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

app_name = 'stat'
urlpatterns = [
    path('', views.StatisticalListView.as_view(), name='list'),
    path('<int:pk>/', views.StatisticalDetailView.as_view(), name='detail'),
    path('<int:pk>/refreshed/', views.StatisticalRefreshedDetailView.as_view(), name='detail-refreshed'),
    path('original-PDFs-list/', views.OriginalPDFListView.as_view(), name='original-PDFs-list'),
    path('original-PDFs-list/refreshed/', views.OriginalPDFRefreshedListView.as_view(), name='original-PDFs-list-refreshed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)