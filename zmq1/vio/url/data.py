from django.urls import path
from ..views import data

urlpatterns = [
    path('profile_file/', data.profile_file, name='profile_file'),
]