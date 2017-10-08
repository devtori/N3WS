from django.contrib import admin
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):

    list_display = ['id', 'num', 'keyword1', 'keyword2', 'keyword3']
