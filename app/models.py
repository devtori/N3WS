# -*- coding: utf-8 -*-

from django.db import models

class News(models.Model):
    class Meta:
        verbose_name = "News"
        verbose_name_plural = "Newses"

    url = models.TextField(null=True, blank=True, verbose_name="주소")
    content = models.TextField(null=True, blank=True)
    keyword1 = models.CharField(max_length=30, default="", blank=True, null=True, verbose_name="키워드1")
    keyword2 = models.CharField(max_length=30, default="", blank=True, null=True, verbose_name="키워드2")
    keyword3 = models.CharField(max_length=30, default="", blank=True, null=True, verbose_name="키워드3")



class Cache(models.Model):
    class Meta:
        verbose_name = "Cache"
        verbose_name_plural = "Caches"

    word = models.CharField(max_length=30, default="", blank=True, null=True, verbose_name="선택 키워드")
    url = url = models.TextField(null=True, blank=True, verbose_name="주소")
    sentence1 = models.TextField(null=True, blank=True, verbose_name="문장1")
    sentence2 = models.TextField(null=True, blank=True, verbose_name="문장2")
    sentence3 = models.TextField(null=True, blank=True, verbose_name="문장3")
    num = models.IntegerField(null=True, blank=True, verbose_name="Number")
