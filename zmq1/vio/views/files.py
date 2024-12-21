import os
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from ..forms.data import DataFileForm
from ..models import DataFile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, FileResponse


@login_required
def profile_file(request):
    user_files = DataFile.objects.filter(author=request.user).order_by('-uploaded_at')
    if request.method == 'POST':
        form = DataFileForm(request.POST, request.FILES)
        if form.is_valid():
            data_file = form.save(commit=False)
            data_file.author = request.user
            data_file.save()
            messages.success(request, '上传成功')
            return redirect('profile_file')
    else:
        form = DataFileForm()

    return render(request, 'users/profile_file.html', {
        'files': user_files,
        'form': form
    })

@login_required
# 文件下载
def download_file(request, file_id):
    file_instance = get_object_or_404(DataFile, id=file_id, author=request.user)  # 确保文件属于当前用户
    file_path = file_instance.file.path  # 获取文件路径
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_instance.original_name)
    else:
        raise HttpResponseForbidden('文件不存在！')

@login_required
# 文件删除
def delete_file(request, file_id):
    file_instance = get_object_or_404(DataFile, id=file_id, author=request.user)  # 确保文件属于当前用户
    file_path = file_instance.file.path  # 获取文件路径
    file_instance.delete()  # 删除数据库中的记录
    if os.path.exists(file_path):
        os.remove(file_path)  # 删除文件系统中的实际文件
    messages.success(request, '文件已删除！')

    return redirect('profile_file')
