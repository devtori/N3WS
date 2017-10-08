# -*- coding: utf-8 -*-

from django.db import models

class News(models.Model):

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "Newses"

    num = models.IntegerField()
    url = models.TextField()
    content = models.TextField()
    keyword1 = models.CharField(max_length=30, default="", blank=True, null=True, verbose_name="키워드1")
    keyword2 = models.CharField(max_length=30, default="", blank=True, null=True, verbose_name="키워드2")
    keyword3 = models.CharField(max_length=30, default="", blank=True, null=True, verbose_name="키워드3")
    sentence1 = models.TextField(null=True, blank=True)
    sentence2 = models.TextField(null=True, blank=True)
    sentence3 = models.TextField(null=True, blank=True)
