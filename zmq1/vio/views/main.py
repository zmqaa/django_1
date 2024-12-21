from django.shortcuts import render, redirect, get_object_or_404
from ..models import Article, AccessLog
from django.db.models import Q  # 支持复杂查询
from ..utils.weather_utils import get_weather_data
from django_ratelimit.decorators import ratelimit
from django_ratelimit.core import is_ratelimited

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


@ratelimit(key='ip', rate='5/m', block=False)  # block=False 表示不直接阻止请求
def weather_view(request):
    # 检测是否超出限制
    is_limited = is_ratelimited(request, fn=weather_view, key='ip', rate='5/m', method=['POST'], increment=True)
    weather_data = None
    error_message = None

    if is_limited:  # 如果超出限制
        error_message = "查询过于频繁，每分钟仅允许查询 5 次，请稍后再试。"
    elif request.method == 'POST':
        city = request.POST.get('city', '440100')  # 获取城市信息
        weather_data = get_weather_data(city)  # 调用天气数据 API

    return render(request, 'weather.html', {
        'weather_data': weather_data,
        'error_message': error_message,
    })
