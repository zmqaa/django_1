from django.shortcuts import render, redirect, get_object_or_404
from ..models import Article, AccessLog
from django.db.models import Q  # 支持复杂查询

def index(request):
    # articles = Article.objects.all().order_by('-created_at')
    # return render(request, 'index.html', {'articles': articles})
    query = request.GET.get('q')
    # icontains 是大小写不敏感的部分匹配查询。
    # Q 允许在查询中使用逻辑 OR。
    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')
    else:
        articles = Article.objects.all().order_by('-created_at')

    # 排行
    popular_articles = Article.objects.order_by('-views')[:10]




    return render(request, 'index.html', {
        'articles': articles,
        'query': query,
        'popular_articles': popular_articles,
    })

def log(request):

    logs = AccessLog.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'logs.html', {'logs':logs})
