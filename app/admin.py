from django.contrib import admin
from .models import News
from .models import Cache

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'url','content', 'keyword1', 'keyword2', 'keyword3']

@admin.register(Cache)
class CacheAdmin(admin.ModelAdmin):
    list_display = ['word', 'url', 'sentence1', 'sentence2', 'sentence3']
