from django.contrib import admin
from .models import Article, Comment, Profile, DataFile, AccessLog, Tag
# Register your models here.

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(DataFile)
admin.site.register(AccessLog)
admin.site.register(Tag)