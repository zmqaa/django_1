import os
import tempfile
import uuid

def upload_to(instance, filename):
    # 提取文件扩展名
    extension = filename.rsplit('.')[-1]
    # 生成唯一文件名
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    # 存储到 'uploads/' 目录下
    return os.path.join('uploads', unique_filename)


