from django.contrib import messages
from django.shortcuts import render, redirect
from ..forms.data import DataFileForm
from ..models import DataFile

def upload_file(request):
    if request.method == 'POST':
        form = DataFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '上传成功')