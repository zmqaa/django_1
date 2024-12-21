from django.urls import path
from ..views import data

urlpatterns = [
    path('data_shape/<int:file_id>/', data.data_shape, name='data_shape'),
    path('visualization/<int:file_id>/', data.visualization, name='visualization'),
    path('process/<int:file_id>/', data.process_data_view, name='process_data'),
]