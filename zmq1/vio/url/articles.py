from django.urls import path
from ..views import articles

urlpatterns = [
    path('articles/<int:article_id>/', articles.article_detail, name='article_detail'),
    path('articles/create/', articles.article_create, name='article_create'),
    path('article/update/<int:article_id>/', articles.article_update, name='article_update'),
    path('articles/delete/<int:article_id>/', articles.article_delete, name='article_delete'),
    path('comment/create/<int:article_id>/', articles.comment_create, name='comment_create'),
    path('comment/delete/<int:comment_id>/', articles.comment_delete, name='comment_delete'),
    path('like/<int:article_id>/', articles.like_article, name='like_article'),
]
