from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms.data import DataFileForm
from ..models import DataFile

@login_required
def profile_file(request):
    user_files = DataFile.objects.filter(author=request.user)
    if request.method == 'POST':
        form = DataFileForm(request.POST, request.FILES)
        if form.is_valid():
            data_file = form.save(commit=False)
            data_file.author = request.user
            data_file.save()
            return redirect('profile_file')
    else:
        form = DataFileForm()

    return render(request, 'users/profile_file.html', {
        'files': user_files,
        'form': form
    })

from django.http import HttpResponseForbidden, FileResponse
@login_required
def file_download(request, file_id):
    try:
        data_file = DataFile.objects.get(pk=file_id, author=request.user)
    except DataFile.DoesNotExist:
        messages.error(request, '无权下载')
    # as_attachment=True: 指示浏览器将文件作为附件下载，而不是直接在浏览器中显示。
    # filename=data_file.original_name: 指定下载时的文件名为 data_file.original_name。
    response = FileResponse(open(data_file.name, 'rb'), as_attachment=True, filename=data_file.original_name)
    return response
