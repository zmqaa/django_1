from django.urls import path, include
from .views import users, main, articles


# urlpatterns = [
#     path('', main.index, name='index'),
#     path('register/', users.register, name='register'), # name可以用来在前端中反代到视图
#     path('login/', users.login_view, name='login'),
#     path('logout/', users.logout_view, name='logout'),
#     path('profile/', users.profile, name='profile'),
#     path('articles/<int:article_id>/', articles.article_detail, name='article_detail'),
#     path('articles/create/', articles.article_create, name='article_create'),
#     path('articles/delete/<int:article_id>/', articles.article_delete, name='article_delete'),
#     path('comment/create/<int:article_id>/', articles.comment_create, name='comment_create'),
#     path('comment/delete/<int:comment_id>/', articles.comment_delete, name='comment_delete'),
# ]

urlpatterns = [
    path('', main.index, name='index'),
    path('log/', main.log, name='log'),
    path('users/', include('vio.url.users')),
    path('articles/', include('vio.url.articles')),
    path('data/', include('vio.url.data')),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)