from django.shortcuts import render, redirect, get_object_or_404
from ..models import Article, Comment
from ..forms.articles import ArticleForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    # 触发了视图浏览次数就加一
    article.views += 1
    article.save()

    return render(request, 'articles/article_detail.html', {'article': article})

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, '发布成功')
            return redirect('index')
    else:
        form = ArticleForm()

    return render(request, 'articles/create_article.html', {'form': form})

@login_required
def article_update(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if article.author != request.user:
        messages.error(request, '无权限编辑')
        return redirect('index')

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)  # instance加载现有文章
        if form.is_valid():
            form.save()
            messages.success(request, '修改成功')
            return redirect('article_detail', article_id=article_id)

    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/article_update.html', {'form': form, 'article': article})

@login_required
def article_delete(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if article.author == request.user:
        article.delete()
        return redirect('index')
    else:
        return redirect('index')

def comment_create(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            messages.success(request, '评论成功')
            return redirect('article_detail', article_id=article_id)
    else:
        form = CommentForm()

    return render(request, 'articles/article_detail.html', {'form': form, 'article': article})

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        comment.delete()
        messages.success(request, '删除评论成功')
        return redirect('article_detail', article_id=comment.article.id)
    else:
        messages.error(request, '无权限')
        return redirect('article_detail', article_id=comment.article.id)


# 点赞
from django.http import JsonResponse
from django.views.decorators.http import require_POST
@require_POST  # 确保只能通过 POST 方法访问
def like_article(request, article_id):
    # 根据 ID 获取文章
    article = get_object_or_404(Article, id=article_id)

    # 点赞数加 1
    article.likes += 1
    article.save()

    # 返回 JSON 数据给前端，包含最新点赞数
    return JsonResponse({'likes': article.likes})

