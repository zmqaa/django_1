from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from ..forms.users import RegisterForm, LoginForm
from ..forms.profile import ProfileForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from ..models import Article, Comment, Profile


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 表单验证是通过调用 form.is_valid() 方法触发的。
            # 这个方法会执行以下几个步骤：
            # 调用 form.full_clean() 方法。
            # 检查每个字段的验证规则。
            # 如果字段验证通过，将清理后的数据存储到 form.cleaned_data。
            # 如果有字段验证失败，将错误信息存储到 form.errors。
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # 保存到数据库
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            messages.success(request, f'注册成功')
            return redirect('login')
        else:
            messages.error(request, '注册失败')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, '登录成功')
                return redirect('index')
            else:
                messages.error(request, '用户名或密码错误')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, '退出登录')
    return redirect('index')  # 登出后跳转到首页

def profile(request):
    user = request.user
    articles = Article.objects.all().filter(author=request.user)
    comments = Comment.objects.all().filter(author=request.user)
    return render(request, 'users/profile.html', {
        'user': user,
        'articles': articles,
        'comments': comments
    })

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '修改成功')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/profile_edit.html', {'form': form})