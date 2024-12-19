from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="文章标题")   # verbose是admin后台显示的名字
    content = models.TextField(verbose_name="文章内容")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles", verbose_name="作者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    views = models.PositiveIntegerField(default=0)  # 浏览次数
    likes = models.PositiveIntegerField(default=0) # 点赞次数
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):  # 定义对象的字符串表示形式，常用于 Django Admin 和交互式命令行中显示模型对象的简短描述。
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE, verbose_name="文章")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="作者")
    content = models.TextField(verbose_name="评论内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return f'{self.author} on {self.article}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/1.jpg')
    # ImangeField 要下载pillow包来处理
    dis_name = models.CharField(max_length=100, blank=True, verbose_name='名称')
    def __str__(self):
        return self.user.username

# 自动创建profile和保存
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)   # post_save在User模型保存后触发信号
def create_user_profile(sender, instance, created, **kwargs):   # 用户创建时自动创建profile实例
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):  # 用户更新时，profile也同步保存
    instance.profile.save()

from .utils.file_utils import upload_to
class DataFile(models.Model):
    file = models.FileField(upload_to=upload_to)
    original_name = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='data_files', default=1)

    def __str__(self):
        return f'{self.author.username}-{self.file.name}'

    def save(self, *args, **kwargs):
        if not self.original_name and self.file:
            self.original_name = self.file.name.split('/')[-1]
        super().save(*args, **kwargs)

class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(verbose_name='IP_地址') # 自带检验合法的ip
    path = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.path} - {self.created_at}"

