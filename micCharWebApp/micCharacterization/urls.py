from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

app_name = 'mic-characterization'
urlpatterns = [
    path('', views.MicDataRecordListView.as_view(), name='mic-data-record-list'),
    path('new/', views.MicDataRecordCreateView.as_view(), name='mic-data-record-create'),
    path('<int:pk>/update/', views.MicDataRecordUpdateView.as_view(), name='mic-data-record-update'),
    path('<int:pk>/delete/', views.MicDataRecordDeleteView.as_view(), name='mic-data-record-confirm-delete'),
    path('logs/', views.LogListView.as_view(), name='log-list'),
    path('logs/<int:pk>/delete/', views.LogDeleteView.as_view(), name='log-confirm-delete'),
    path('logs/delete/all/', views.delete_all_logs, name='log-confirm-delete-all'),
    path('important-concepts/', views.ImportantConceptsView.as_view(), name='concepts'),
    path('acoustic-propagation/', views.AcousticPropagationView.as_view(), name='acoustic-prop'),
    path('test/', views.TestView.as_view(), name='test-view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)