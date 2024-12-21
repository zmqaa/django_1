from django.urls import path
from ..views import files

urlpatterns = [
    path('profile_file/', files.profile_file, name='profile_file'),
    path('download/<int:file_id>/', files.download_file, name='download_file'),  # 下载文件
    path('delete/<int:file_id>/', files.delete_file, name='delete_file'),  # 删除文件
]