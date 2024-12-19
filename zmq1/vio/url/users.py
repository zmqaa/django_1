from django.urls import path
from ..views import users

urlpatterns = [
    path('register/', users.register, name='register'), # name可以用来在前端中反代到视图
    path('login/', users.login_view, name='login'),
    path('logout/', users.logout_view, name='logout'),
    path('profile/', users.profile, name='profile'),
    path('profile/edit/', users.profile_edit, name='profile_edit'),
]